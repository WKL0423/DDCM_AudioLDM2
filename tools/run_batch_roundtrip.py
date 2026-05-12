#!/usr/bin/env python3
"""
Batch AudioLDM2 DDCM roundtrip + objective metrics for every entry in manifest.json.

Requires: HUGGINGFACE_HUB_CACHE (defaults to ~/.cache/huggingface/hub), ddcm torch env.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import statistics as stats
import subprocess
from pathlib import Path


def find_decomp(output_dir: Path, stem: str) -> Path:
    matches = list(output_dir.rglob(f"{stem}_decomp.wav"))
    if not matches:
        raise FileNotFoundError(f"No {stem}_decomp.wav under {output_dir}")
    return matches[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True, help="Passed to audio_compression --output_dir")
    ap.add_argument("--aggregate-json", type=Path, required=True)
    ap.add_argument(
        "--aggregate-md",
        type=Path,
        default=None,
        help="If set, write standard Markdown report via tools/render_batch_aggregate_report.py",
    )
    ap.add_argument(
        "--aggregate-md-title",
        type=str,
        default=None,
        help="Title for --aggregate-md (default: derived from output-dir name)",
    )
    ap.add_argument(
        "--python",
        type=str,
        default=os.environ.get("DDCM_PYTHON", shutil.which("python3") or "python3"),
        help="Interpreter for audio_compression subprocess (override with DDCM_PYTHON).",
    )
    ap.add_argument("--skip-existing", action="store_true", help="Skip roundtrip if decomp wav already exists")
    ap.add_argument(
        "--hf-hub-cache",
        type=str,
        default=os.environ.get(
            "HUGGINGFACE_HUB_CACHE",
            str(Path.home() / ".cache" / "huggingface" / "hub"),
        ),
    )

    ap.add_argument("-T", dest="T", type=int, default=999)
    ap.add_argument("-K", dest="K", type=int, default=1000)
    ap.add_argument("--pursuit-noises", type=int, default=2)
    ap.add_argument("--pursuit-coef-bits", type=int, default=4)
    ap.add_argument("--t0", type=int, default=999)
    ap.add_argument("--t1", type=int, default=0)
    ap.add_argument("--eta", type=float, default=1.0)
    ap.add_argument("--eta-late", type=float, default=0.3)
    ap.add_argument("--eta-switch-t", type=int, default=200)
    ap.add_argument("--score-mode", type=str, default="blend")
    ap.add_argument("--score-blend-lambda", type=float, default=0.5)
    ap.add_argument("--score-mode-late", type=str, default="")
    ap.add_argument("--score-switch-t", type=int, default=-1)
    ap.add_argument("--model-id", dest="model_id", type=str, default="cvssp/audioldm2-music")
    args = ap.parse_args()

    os.environ["HUGGINGFACE_HUB_CACHE"] = args.hf_hub_cache

    repo = Path(__file__).resolve().parents[1]
    py = args.python
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for it in manifest["items"]:
        audio_id = it["id"]
        p = it.get("abs_path") or it.get("path")
        if not p:
            raise ValueError(f"manifest item {audio_id} missing abs_path/path")
        inp = Path(p)
        stem = inp.stem
        try:
            dec = find_decomp(args.output_dir, stem)
            exists = dec.exists()
        except FileNotFoundError:
            exists = False

        if not (args.skip_existing and exists):
            cmd = [
                py,
                str(repo / "audio_compression.py"),
                "roundtrip",
                "--output_dir",
                str(args.output_dir),
                "--input_path",
                str(inp),
                "--model_id",
                args.model_id,
                "-T",
                str(args.T),
                "-K",
                str(args.K),
                "--pursuit-noises",
                str(args.pursuit_noises),
                "--pursuit-coef-bits",
                str(args.pursuit_coef_bits),
                "--t_range",
                str(args.t0),
                str(args.t1),
                "--eta",
                str(args.eta),
                "--eta-late",
                str(args.eta_late),
                "--eta-switch-t",
                str(args.eta_switch_t),
                "--score-mode",
                args.score_mode,
                "--score-blend-lambda",
                str(args.score_blend_lambda),
            ]
            if args.score_mode_late:
                cmd += ["--score-mode-late", args.score_mode_late, "--score-switch-t", str(args.score_switch_t)]
            subprocess.run(cmd, check=True, cwd=str(repo))

        dec = find_decomp(args.output_dir, stem)
        mpath = args.output_dir / f"{audio_id}_metrics.json"
        subprocess.run(
            [
                py,
                str(repo / "tools/compare_audio_metrics.py"),
                "--ref",
                str(inp),
                "--test",
                str(dec),
                "--out-json",
                str(mpath),
            ],
            check=True,
            cwd=str(repo),
        )
        m = json.loads(mpath.read_text(encoding="utf-8"))

        out_inner = dec.parent
        ij = out_inner / f"{stem}_noise_indices.json"
        ib = out_inner / f"{stem}_noise_indices.bin"
        json_bytes = ij.stat().st_size if ij.exists() else 0
        bin_bytes = ib.stat().st_size if ib.exists() else 0

        rows.append(
            {
                "audio": audio_id,
                "input_path": str(inp),
                "out_dir": str(out_inner),
                "mel_db_mae": m.get("mel_db_mae"),
                "stft_mag_mse": m.get("stft_mag_mse"),
                "mel_db_mae_low_band": m.get("mel_db_mae_low_band"),
                "mel_db_mae_high_band": m.get("mel_db_mae_high_band"),
                "waveform_mse": m.get("waveform_mse"),
                "snr_db": m.get("snr_db"),
                "pearson_corr": m.get("pearson_corr"),
                "spectral_centroid_l1": m.get("spectral_centroid_l1"),
                "json_bytes": json_bytes,
                "bin_bytes": bin_bytes,
                "total_bytes": json_bytes + bin_bytes,
            }
        )

    agg = {
        "num_files": len(rows),
        "mean_mel_db_mae": float(stats.mean(r["mel_db_mae"] for r in rows)),
        "median_mel_db_mae": float(stats.median(r["mel_db_mae"] for r in rows)),
        "mean_stft_mag_mse": float(stats.mean(r["stft_mag_mse"] for r in rows)),
        "median_stft_mag_mse": float(stats.median(r["stft_mag_mse"] for r in rows)),
    }
    payload = {
        "manifest": str(args.manifest),
        "output_dir": str(args.output_dir),
        "params": {
            "T": args.T,
            "K": args.K,
            "eta": args.eta,
            "eta_late": args.eta_late,
            "eta_switch_t": args.eta_switch_t,
            "score_mode": args.score_mode,
            "model_id": args.model_id,
        },
        "rows": rows,
        "aggregate": agg,
    }
    args.aggregate_json.parent.mkdir(parents=True, exist_ok=True)
    args.aggregate_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({"wrote": str(args.aggregate_json), "aggregate": agg}, indent=2))

    if args.aggregate_md is not None:
        title = args.aggregate_md_title or f"Batch report: {args.output_dir.name}"
        subprocess.run(
            [
                py,
                str(repo / "tools/render_batch_aggregate_report.py"),
                "--aggregate-json",
                str(args.aggregate_json),
                "--out-md",
                str(args.aggregate_md),
                "--title",
                title,
            ],
            check=True,
            cwd=str(repo),
        )


if __name__ == "__main__":
    main()
