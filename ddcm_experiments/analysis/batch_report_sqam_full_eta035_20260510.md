# SQAM-6 full batch (eta_late=0.35@200)

- **Manifest**: `datasets/ebu_sqam_16k_subset/manifest.json`
- **Output dir**: `runs/sqam_full_eta035_sw200_20260510`

## Params

```json
{
  "T": 999,
  "K": 1000,
  "eta": 1.0,
  "eta_late": 0.35,
  "eta_switch_t": 200,
  "score_mode": "blend",
  "model_id": "cvssp/audioldm2-music"
}
```

## Aggregate (mean + median)

| Metric | Mean | Median |
|--------|-----:|-------:|
| `mel_db_mae` | 5.6243 | 4.1695 |
| `stft_mag_mse` | 0.5723 | 0.4341 |

## Mean vs median (outliers)

- **Highest `mel_db_mae`**: `sqam_01_16k` (12.7069).
- **Batch mean** `mel_db_mae`: 5.6243; **median**: 4.1695.
- **Note**: Mean is notably above median — interpret **mean with the table**, not alone; SQAM-sized sets are especially sensitive to one difficult item.

## Per-track

| id | mel_db_mae | stft_mag_mse | mel_low | mel_high |
|----|------------:|-------------:|--------:|---------:|
| `sqam_01_16k` | 12.7069 | 1.6075 | 14.271 | 11.943 |
| `sqam_32_16k` | 6.1079 | 0.1531 | 5.204 | 6.549 |
| `sqam_34_16k` | 3.3536 | 0.2277 | 4.815 | 2.640 |
| `sqam_49_16k` | 4.1534 | 0.4796 | 4.888 | 3.794 |
| `sqam_50_16k` | 4.1857 | 0.5771 | 4.890 | 3.842 |
| `sqam_52_16k` | 3.2386 | 0.3885 | 4.081 | 2.827 |
