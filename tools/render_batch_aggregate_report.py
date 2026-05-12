#!/usr/bin/env python3
"""
Render a standard Markdown report from run_batch_roundtrip aggregate.json (or compatible).

Includes: params summary, mean + median, per-track table, and for small / skewed sets a
note on which item(s) dominate the mean (esp. SQAM).
"""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any


def _mean(xs: list[float]) -> float:
    return float(sum(xs) / len(xs)) if xs else float("nan")


def _ensure_aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    mels = [float(r["mel_db_mae"]) for r in rows if r.get("mel_db_mae") is not None]
    stfts = [float(r["stft_mag_mse"]) for r in rows if r.get("stft_mag_mse") is not None]
    return {
        "num_files": len(rows),
        "mean_mel_db_mae": _mean(mels),
        "median_mel_db_mae": float(statistics.median(mels)) if mels else float("nan"),
        "mean_stft_mag_mse": _mean(stfts),
        "median_stft_mag_mse": float(statistics.median(stfts)) if stfts else float("nan"),
    }


def _dominance_note(rows: list[dict[str, Any]], agg: dict[str, Any]) -> str:
    if not rows:
        return ""
    by_mel = sorted(rows, key=lambda r: float(r.get("mel_db_mae") or 0), reverse=True)
    top = by_mel[0]
    tid = top.get("audio", "?")
    mel = float(top["mel_db_mae"])
    mean_mel = agg["mean_mel_db_mae"]
    med_mel = agg["median_mel_db_mae"]
    lines = [
        "## Mean vs median (outliers)",
        "",
        f"- **Highest `mel_db_mae`**: `{tid}` ({mel:.4f}).",
        f"- **Batch mean** `mel_db_mae`: {mean_mel:.4f}; **median**: {med_mel:.4f}.",
    ]
    if mean_mel > med_mel + 0.5:
        lines.append(
            "- **Note**: Mean is notably above median — interpret **mean with the table**, not alone; "
            "SQAM-sized sets are especially sensitive to one difficult item."
        )
    elif len(rows) <= 8:
        lines.append(
            "- **Note**: Small-N set — prefer **median** and per-track rows for decisions; mean is auxiliary."
        )
    return "\n".join(lines)


def render_markdown(payload: dict[str, Any], title: str | None = None) -> str:
    rows = payload.get("rows") or []
    agg = payload.get("aggregate") or {}
    if "median_mel_db_mae" not in agg and rows:
        agg = {**agg, **_ensure_aggregate(rows)}
    elif rows and agg.get("median_mel_db_mae") is None:
        agg = {**agg, **_ensure_aggregate(rows)}

    manifest = payload.get("manifest", "")
    out_dir = payload.get("output_dir", "")
    params = payload.get("params") or payload.get("config")

    t = title or "Batch aggregate report"
    lines = [
        f"# {t}",
        "",
        f"- **Manifest**: `{manifest}`",
        f"- **Output dir**: `{out_dir}`",
        "",
    ]
    if params:
        lines += ["## Params", "", "```json", json.dumps(params, indent=2), "```", ""]

    lines += [
        "## Aggregate (mean + median)",
        "",
        "| Metric | Mean | Median |",
        "|--------|-----:|-------:|",
        f"| `mel_db_mae` | {agg.get('mean_mel_db_mae', float('nan')):.4f} | {agg.get('median_mel_db_mae', float('nan')):.4f} |",
        f"| `stft_mag_mse` | {agg.get('mean_stft_mag_mse', float('nan')):.4f} | {agg.get('median_stft_mag_mse', float('nan')):.4f} |",
        "",
    ]

    lines.append(_dominance_note(rows, agg))
    lines.append("")

    lines += [
        "## Per-track",
        "",
        "| id | mel_db_mae | stft_mag_mse | mel_low | mel_high |",
        "|----|------------:|-------------:|--------:|---------:|",
    ]
    for r in sorted(rows, key=lambda x: str(x.get("audio", ""))):
        lo = r.get("mel_db_mae_low_band")
        hi = r.get("mel_db_mae_high_band")
        lo_s = f"{lo:.3f}" if lo is not None else ""
        hi_s = f"{hi:.3f}" if hi is not None else ""
        lines.append(
            f"| `{r.get('audio','')}` | {float(r.get('mel_db_mae', 0)):.4f} | "
            f"{float(r.get('stft_mag_mse', 0)):.4f} | {lo_s} | {hi_s} |"
        )
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aggregate-json", type=Path, required=True)
    ap.add_argument("--out-md", type=Path, required=True)
    ap.add_argument("--title", type=str, default=None)
    args = ap.parse_args()

    payload = json.loads(args.aggregate_json.read_text(encoding="utf-8"))
    md = render_markdown(payload, title=args.title)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text(md, encoding="utf-8")
    print(json.dumps({"wrote": str(args.out_md)}, indent=2))


if __name__ == "__main__":
    main()
