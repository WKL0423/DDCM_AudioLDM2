# Full-batch validation: `eta_late=0.35` @ `eta_switch_t=200`

Subset sweep ([eta_sweep_subset_summary_20260510.md](eta_sweep_subset_summary_20260510.md)) picked **`eta0.35_sw200`** as the Pareto front on 7 clips. This document reports **MUSAN music 20** and **SQAM subset 6** with that setting versus the frozen baseline **`eta_late=0.3` @ 200** ([musan_music_batch_metrics_20260506.md](../../runs/musan_music_batch_baseline_etaLate/musan_music_batch_metrics_20260506.md), [sqam_batch_metrics_20260505.md](../../runs/sqam_batch_baseline_etaLate/sqam_batch_metrics_20260505.md)).

**Runner**: [tools/run_batch_roundtrip.py](../../tools/run_batch_roundtrip.py) with `HUGGINGFACE_HUB_CACHE=/home/wang/.cache/huggingface/hub`, `T=999`, `K=1000`, `P=2`, `score_mode=blend(0.5)`, `cvssp/audioldm2-music`.

## MUSAN-20 (`datasets/musan_music_16k_benchmark20/manifest.json`)

| Config | mean `mel_db_mae` | median `mel_db_mae` | mean `stft_mag_mse` | median `stft_mag_mse` |
|--------|-------------------|---------------------|----------------------|------------------------|
| Baseline `1.0→0.3@200` | 3.767 | 3.776 | 2.009 | 0.927 |
| Candidate `1.0→0.35@200` | **3.756** | **3.733** | 2.009 | **0.915** |

- **Aggregate file**: [runs/musan_full_eta035_sw200_20260510/aggregate.json](../../runs/musan_full_eta035_sw200_20260510/aggregate.json)

On this benchmark, **`eta_late=0.35` is slightly better on the primary `mel_db_mae` (mean and median)** with **similar** mean `stft_mag_mse` and a **small** median `stft_mag_mse` improvement.

## SQAM-6 (`datasets/ebu_sqam_16k_subset/manifest.json`)

| Config | mean `mel_db_mae` | median `mel_db_mae` | mean `stft_mag_mse` | median `stft_mag_mse` |
|--------|-------------------|---------------------|----------------------|------------------------|
| Baseline `1.0→0.3@200` | 5.481 | 3.797 | 0.535 | 0.373 |
| Candidate `1.0→0.35@200` | 5.624 | 4.170 | 0.572 | 0.434 |

- **Aggregate file**: [runs/sqam_full_eta035_sw200_20260510/aggregate.json](../../runs/sqam_full_eta035_sw200_20260510/aggregate.json)

SQAM is **dominated by one difficult item** (`sqam_01_16k`); the candidate is **marginally worse on mean `mel_db_mae` and mean `stft_mag_mse`** here. Treat SQAM as a **sanity / stress** check rather than the sole gate for music preset tuning.

## Recommendation

- For **MUSAN-shaped music** objectives (`mel_db_mae` primary, `stft_mag_mse` secondary), **`eta_late=0.35` @ 200** is a **reasonable successor** to `0.3` on the full 20-track set.
- **Subjective follow-up (7-clip MUSAN subset, 0.30 vs 0.35):** blind AB on the same hard/easy subset favors **`eta_late=0.30` in 5 of 7 trials** vs **0.35 in 2** — see [musan_listening_ab_protocol_20260511.md](musan_listening_ab_protocol_20260511.md). Prefer **0.35** when optimizing reported means; prefer **0.30** when aligning with this listener’s subset preference (and with Guanyu’s dislike of stronger late-η).
