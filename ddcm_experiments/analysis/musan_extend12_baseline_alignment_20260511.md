# MUSAN extend-12 baseline alignment

Second benchmark draw from the same MUSAN music tree, **disjoint** from [musan_music_16k_benchmark20/manifest.json](../../datasets/musan_music_16k_benchmark20/manifest.json).

## How it was built

- Builder: [tools/build_musan_music_extend_manifest.py](../../tools/build_musan_music_extend_manifest.py)
- Manifest: [datasets/musan_music_16k_extend12/manifest.json](../../datasets/musan_music_16k_extend12/manifest.json) (`selection_seed=20260511`, **12** clips).
- Run: [runs/musan_extend12_baseline_eta030_20260511/aggregate.json](../../runs/musan_extend12_baseline_eta030_20260511/aggregate.json) with **`T999_K1000_P2`**, **`eta_late=0.3`**, **`eta_switch_t=200`**, same flags as the frozen music baseline.

## Alignment vs MUSAN-20 baseline (same preset)

| Set | n | mean `mel_db_mae` | median `mel_db_mae` | mean `stft_mag_mse` | median `stft_mag_mse` |
|-----|--:|------------------:|--------------------:|--------------------:|----------------------:|
| Benchmark20 (eta 0.3@200) | 20 | 3.767 | 3.776 | 2.009 | 0.927 |
| **Extend12** (eta 0.3@200) | 12 | **3.976** | **3.977** | **1.194** | **0.881** |

Interpretation: metrics are **the same order of magnitude**; extend-12 is **slightly harder on `mel_db_mae`** on this random draw and **lower mean `stft_mag_mse`** (distribution differs; do not compare raw means across sets as “better/worse codec”, only as **sanity that the pipeline generalizes**).

Standard report (mean, median, per-track, outlier note): [batch_report_musan_extend12_baseline_eta030_20260511.md](batch_report_musan_extend12_baseline_eta030_20260511.md).
