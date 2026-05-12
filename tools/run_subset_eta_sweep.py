#!/usr/bin/env python3
"""Small eta/eta-switch sweep on a fixed manifest subset; aggregates compare_audio_metrics JSON from stdout."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path


def find_decomp(output_dir: Path, stem: str) -> Path:
    matches = list(output_dir.rglob(f"{stem}_decomp.wav"))
    if not matches:
        raise FileNotFoundError(f"No decomp for stem={stem} under {output_dir}")
    return matches[0]


def run_one(py: str, repo: Path, wav: Path, out_root: Path, eta_late: float, eta_switch: int) -> None:
    out_root.mkdir(parents=True, exist_ok=True)
    cmd = [
        py,
        str(repo / "audio_compression.py"),
        "roundtrip",
        "--output_dir",
        str(out_root),
        "--input_path",
        str(wav),
        "--model_id",
        "cvssp/audioldm2-music",
        "-T",
        "999",
        "-K",
        "1000",
        "--pursuit-noises",
        "2",
        "--pursuit-coef-bits",
        "4",
        "--t_range",
        "999",
        "0",
        "--eta",
        "1.0",
        "--eta-late",
        str(eta_late),
        "--eta-switch-t",
        str(eta_switch),
        "--score-mode",
        "blend",
        "--score-blend-lambda",
        "0.5",
    ]
    subprocess.run(cmd, check=True, cwd=str(repo))


def metrics(py: str, repo: Path, ref: Path, test: Path) -> dict:
    p = subprocess.run(
        [py, str(repo / "tools/compare_audio_metrics.py"), "--ref", str(ref), "--test", str(test)],
        cwd=str(repo),
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(p.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--python", type=str, default="/home/wang/miniconda3/envs/ddcm/bin/python")
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--ids", type=str, required=True, help="Comma-separated manifest ids, e.g. musan_music_03,musan_music_05")
    ap.add_argument("--out", type=Path, required=True, help="Output JSON path")
    args = ap.parse_args()

    os.environ.setdefault("HUGGINGFACE_HUB_CACHE", "/home/wang/.cache/huggingface/hub")

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    want = set(x.strip() for x in args.ids.split(",") if x.strip())
    items = [it for it in manifest["items"] if it["id"] in want]
    if len(items) != len(want):
        missing = want - {it["id"] for it in items}
        raise SystemExit(f"Missing ids in manifest: {missing}")

    variants = [
        {"name": "eta0.25_sw200", "eta_late": 0.25, "eta_switch_t": 200},
        {"name": "eta0.35_sw200", "eta_late": 0.35, "eta_switch_t": 200},
        {"name": "eta0.30_sw150", "eta_late": 0.30, "eta_switch_t": 150},
        {"name": "eta0.30_sw250", "eta_late": 0.30, "eta_switch_t": 250},
    ]

    sweep_root = args.out.parent / (args.out.stem + "_runs")
    sweep_root.mkdir(parents=True, exist_ok=True)

    results = {"variants": [], "subset_ids": sorted(want)}
    for v in variants:
        vdir = sweep_root / v["name"]
        rows = []
        for it in items:
            wav = Path(it["abs_path"])
            stem = wav.stem
            run_one(args.python, args.repo, wav, vdir, v["eta_late"], v["eta_switch_t"])
            dec = find_decomp(vdir, stem)
            m = metrics(args.python, args.repo, wav, dec)
            rows.append(
                {
                    "id": it["id"],
                    "input_path": str(wav),
                    "decomp_path": str(dec),
                    "mel_db_mae": m["mel_db_mae"],
                    "stft_mag_mse": m["stft_mag_mse"],
                    "snr_db": m["snr_db"],
                    "pearson_corr": m["pearson_corr"],
                }
            )
        import statistics as st

        results["variants"].append(
            {
                "name": v["name"],
                "eta_late": v["eta_late"],
                "eta_switch_t": v["eta_switch_t"],
                "rows": rows,
                "mean_mel_db_mae": float(st.mean(r["mel_db_mae"] for r in rows)),
                "median_mel_db_mae": float(st.median(r["mel_db_mae"] for r in rows)),
                "mean_stft_mag_mse": float(st.mean(r["stft_mag_mse"] for r in rows)),
                "median_stft_mag_mse": float(st.median(r["stft_mag_mse"] for r in rows)),
            }
        )

    # rank: lower mel mean, then lower stft mean
    ranked = sorted(
        results["variants"],
        key=lambda x: (x["mean_mel_db_mae"], x["mean_stft_mag_mse"]),
    )
    results["ranked_variant_names"] = [x["name"] for x in ranked]
    results["best_variant"] = ranked[0]["name"]

    args.out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps({"wrote": str(args.out), "best_variant": results["best_variant"]}, indent=2))


if __name__ == "__main__":
    main()
