#!/usr/bin/env python3
"""
Prepare a blind AB folder for two batch aggregates (same clips, different presets).

Copies references and paired decomp WAVs into ab_session/, randomizes A/B per trial,
writes ab_key.json and scores_template.csv. Multi-listener: each person copies
scores_template.csv to scores_listener_<id>.csv before filling.
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _row_by_id(rows: list[dict]) -> dict[str, dict]:
    return {r["audio"]: r for r in rows}


def _decomp_path(repo: Path, row: dict) -> Path:
    out = Path(row["out_dir"])
    if not out.is_absolute():
        out = repo / out
    stem = Path(row["input_path"]).stem
    matches = list(out.glob(f"{stem}_decomp.wav"))
    if not matches:
        raise FileNotFoundError(f"No {stem}_decomp.wav under {out}")
    return matches[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aggregate-a", type=Path, required=True, help="JSON from run_batch_roundtrip (preset A)")
    ap.add_argument("--aggregate-b", type=Path, required=True, help="JSON from run_batch_roundtrip (preset B)")
    ap.add_argument("--label-a", type=str, required=True, help="e.g. eta_late_0.30")
    ap.add_argument("--label-b", type=str, required=True, help="e.g. eta_late_0.35")
    ap.add_argument("--clip-ids", type=str, required=True, help="Comma-separated audio ids present in both JSONs")
    ap.add_argument("--out-session", type=Path, required=True, help="e.g. runs/foo/ab_session")
    ap.add_argument("--seed", type=int, default=20260511)
    args = ap.parse_args()

    repo = _repo_root()
    ja = json.loads(args.aggregate_a.read_text(encoding="utf-8"))
    jb = json.loads(args.aggregate_b.read_text(encoding="utf-8"))
    ra = _row_by_id(ja["rows"])
    rb = _row_by_id(jb["rows"])
    ids = [x.strip() for x in args.clip_ids.split(",") if x.strip()]
    for i in ids:
        if i not in ra or i not in rb:
            raise SystemExit(f"Missing row for {i} in one of the aggregates")

    session = args.out_session
    session.mkdir(parents=True, exist_ok=True)

    rng = random.Random(args.seed)
    trials_meta = []
    template_rows = ["trial_id,clip_id,preferred_sample,confidence_1_to_5,notes,listener_id"]

    for k, clip_id in enumerate(ids, start=1):
        path_a = _decomp_path(repo, ra[clip_id])
        path_b = _decomp_path(repo, rb[clip_id])
        ref_src = Path(ra[clip_id]["input_path"])
        if not ref_src.is_absolute():
            ref_src = repo / ref_src

        trial_id = f"trial{k}_{clip_id}"
        swap = rng.random() < 0.5
        if swap:
            first, second = path_b, path_a
            label_first, label_second = args.label_b, args.label_a
        else:
            first, second = path_a, path_b
            label_first, label_second = args.label_a, args.label_b

        shutil.copy2(ref_src, session / f"{trial_id}_reference.wav")
        shutil.copy2(first, session / f"{trial_id}_A.wav")
        shutil.copy2(second, session / f"{trial_id}_B.wav")

        trials_meta.append(
            {
                "trial_id": trial_id,
                "clip_id": clip_id,
                "sample_A": label_first,
                "sample_B": label_second,
            }
        )
        template_rows.append(f"{trial_id},{clip_id},,,,")

    key = {
        "seed": args.seed,
        "label_a_config": args.label_a,
        "label_b_config": args.label_b,
        "instructions": "Blind AB vs reference. Listen to *_reference.wav then A vs B. Fill preferred_sample A or B.",
        "trials": trials_meta,
    }
    (session / "ab_key.json").write_text(json.dumps(key, indent=2), encoding="utf-8")
    (session / "scores_template.csv").write_text("\n".join(template_rows) + "\n", encoding="utf-8")
    readme = f"""# MUSAN subset AB ({args.label_a} vs {args.label_b})

## Files
- Per trial: `{{trial_id}}_reference.wav`, `{{trial_id}}_A.wav`, `{{trial_id}}_B.wav`
- Hidden mapping: `ab_key.json` (open only after scoring)

## Scoring
1. Copy `scores_template.csv` to `scores_listener_<your_name>.csv` (multi-listener).
2. For each row: set `preferred_sample` to `A` or `B`, `confidence_1_to_5` (1..5), optional `notes`, your `listener_id`.
3. Primary question: which is **closer to the reference** in timbre and musical noise?

## MOS extension (optional)
Add columns `mos_A_1_to_5` and `mos_B_1_to_5` in your listener CSV if you want absolute quality grades in addition to preference.
"""
    (session / "README_ab.txt").write_text(readme, encoding="utf-8")
    print(json.dumps({"wrote": str(session), "trials": len(ids)}, indent=2))


if __name__ == "__main__":
    main()
