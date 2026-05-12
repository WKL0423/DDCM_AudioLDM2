# MUSAN extend-12 baseline (eta_late=0.30@200)

- **Manifest**: `datasets/musan_music_16k_extend12/manifest.json`
- **Output dir**: `runs/musan_extend12_baseline_eta030_20260511`

## Params

```json
{
  "T": 999,
  "K": 1000,
  "eta": 1.0,
  "eta_late": 0.3,
  "eta_switch_t": 200,
  "score_mode": "blend",
  "model_id": "cvssp/audioldm2-music"
}
```

## Aggregate (mean + median)

| Metric | Mean | Median |
|--------|-----:|-------:|
| `mel_db_mae` | 3.9762 | 3.9768 |
| `stft_mag_mse` | 1.1937 | 0.8810 |

## Mean vs median (outliers)

- **Highest `mel_db_mae`**: `musan_music_ext_12` (4.4396).
- **Batch mean** `mel_db_mae`: 3.9762; **median**: 3.9768.

## Per-track

| id | mel_db_mae | stft_mag_mse | mel_low | mel_high |
|----|------------:|-------------:|--------:|---------:|
| `musan_music_ext_01` | 4.1774 | 1.4828 | 4.589 | 3.977 |
| `musan_music_ext_02` | 3.5893 | 3.1122 | 4.628 | 3.082 |
| `musan_music_ext_03` | 3.7047 | 2.7452 | 4.463 | 3.334 |
| `musan_music_ext_04` | 3.3010 | 1.8595 | 4.291 | 2.817 |
| `musan_music_ext_05` | 4.3587 | 0.6087 | 4.477 | 4.301 |
| `musan_music_ext_06` | 4.3508 | 0.7055 | 4.681 | 4.190 |
| `musan_music_ext_07` | 3.8314 | 0.0730 | 4.448 | 3.530 |
| `musan_music_ext_08` | 3.7732 | 1.9635 | 4.717 | 3.312 |
| `musan_music_ext_09` | 4.2350 | 0.3974 | 4.229 | 4.238 |
| `musan_music_ext_10` | 3.8313 | 0.2615 | 4.864 | 3.327 |
| `musan_music_ext_11` | 4.1221 | 1.0566 | 4.363 | 4.005 |
| `musan_music_ext_12` | 4.4396 | 0.0587 | 5.396 | 3.972 |
