#!/usr/bin/env python3
"""
Build an additional MUSAN-music manifest excluding paths already in benchmark20.

Uses deterministic shuffle(seed) over sorted relative paths for reproducibility.
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-manifest", type=Path, required=True, help="e.g. datasets/musan_music_16k_benchmark20/manifest.json")
    ap.add_argument("--out-manifest", type=Path, required=True)
    ap.add_argument("--count", type=int, default=12, help="Number of additional clips")
    ap.add_argument("--seed", type=int, default=20260511)
    ap.add_argument("--id-prefix", type=str, default="musan_music_ext")
    args = ap.parse_args()

    base = json.loads(args.base_manifest.read_text(encoding="utf-8"))
    source_root = Path(base["source_root"])
    used = {it["relative_path"] for it in base["items"]}

    all_wavs: list[Path] = []
    for p in sorted(source_root.rglob("*.wav")):
        if "ANNOTATIONS" in p.parts or "LICENSE" in p.parts:
            continue
        rel = p.relative_to(source_root).as_posix()
        if rel in used:
            continue
        all_wavs.append(p)

    rng = random.Random(args.seed)
    rng.shuffle(all_wavs)
    picked = all_wavs[: args.count]
    if len(picked) < args.count:
        raise SystemExit(f"Need {args.count} wavs but only {len(picked)} available after exclusion.")

    items = []
    for i, p in enumerate(picked, start=1):
        rel = p.relative_to(source_root).as_posix()
        items.append(
            {
                "id": f"{args.id_prefix}_{i:02d}",
                "relative_path": rel,
                "abs_path": str(p.resolve()),
            }
        )

    out = {
        "dataset": "MUSAN music extended (excludes benchmark20)",
        "source_root": str(source_root),
        "base_manifest": str(args.base_manifest),
        "selection_seed": args.seed,
        "num_selected": len(items),
        "items": items,
    }
    args.out_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.out_manifest.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps({"wrote": str(args.out_manifest), "num_items": len(items)}, indent=2))


if __name__ == "__main__":
    main()
