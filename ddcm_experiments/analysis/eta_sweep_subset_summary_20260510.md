# Eta subset sweep (hard + easy clips)

- **Script**: [tools/run_subset_eta_sweep.py](../../tools/run_subset_eta_sweep.py)
- **Raw results**: [runs/musan_eta_sweep_subset_20260510/sweep_results.json](../../runs/musan_eta_sweep_subset_20260510/sweep_results.json)
- **Subset**: `musan_music_01,03,05,17,18,19,20` (2 easy + high-STFT / mel–STFT disagreement tails)
- **Variants**: `eta_late ∈ {0.25, 0.35}` @ `eta_switch_t=200`, and `eta_late=0.30` @ `eta_switch_t ∈ {150,250}`; base `eta=1.0`, `T999 K1000 P2`, `score_mode=blend(0.5)`.

## Ranking (mean `mel_db_mae`, then mean `stft_mag_mse`)

From `ranked_variant_names` in the JSON:

1. **`eta0.35_sw200`** — **selected as full-set validation candidate** (`best_variant`)
2. `eta0.30_sw250`
3. `eta0.25_sw200`
4. `eta0.30_sw150`

## Full-batch validation (done)

See [full_batch_eta035_validation_20260510.md](full_batch_eta035_validation_20260510.md). Aggregates:

- [runs/musan_full_eta035_sw200_20260510/aggregate.json](../../runs/musan_full_eta035_sw200_20260510/aggregate.json)
- [runs/sqam_full_eta035_sw200_20260510/aggregate.json](../../runs/sqam_full_eta035_sw200_20260510/aggregate.json)

Compared to `eta_late=0.30@200` in [musan_music_batch_metrics_20260506.md](../../runs/musan_music_batch_baseline_etaLate/musan_music_batch_metrics_20260506.md) and [sqam_batch_metrics_20260505.md](../../runs/sqam_batch_baseline_etaLate/sqam_batch_metrics_20260505.md).
