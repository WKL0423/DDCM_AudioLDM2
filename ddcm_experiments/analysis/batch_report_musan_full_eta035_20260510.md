# MUSAN-20 full batch (eta_late=0.35@200)

- **Manifest**: `datasets/musan_music_16k_benchmark20/manifest.json`
- **Output dir**: `runs/musan_full_eta035_sw200_20260510`

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
| `mel_db_mae` | 3.7558 | 3.7326 |
| `stft_mag_mse` | 2.0086 | 0.9154 |

## Mean vs median (outliers)

- **Highest `mel_db_mae`**: `musan_music_03` (5.4511).
- **Batch mean** `mel_db_mae`: 3.7558; **median**: 3.7326.

## Per-track

| id | mel_db_mae | stft_mag_mse | mel_low | mel_high |
|----|------------:|-------------:|--------:|---------:|
| `musan_music_01` | 3.0828 | 0.0476 | 4.358 | 2.460 |
| `musan_music_02` | 4.4740 | 0.8546 | 4.371 | 4.524 |
| `musan_music_03` | 5.4511 | 0.0003 | 6.207 | 5.082 |
| `musan_music_04` | 4.5860 | 1.3342 | 4.447 | 4.654 |
| `musan_music_05` | 2.7260 | 0.0508 | 4.482 | 1.869 |
| `musan_music_06` | 3.4716 | 0.5212 | 4.126 | 3.152 |
| `musan_music_07` | 3.5661 | 0.8787 | 4.135 | 3.288 |
| `musan_music_08` | 3.9764 | 0.9177 | 4.083 | 3.925 |
| `musan_music_09` | 3.7971 | 1.2251 | 4.422 | 3.492 |
| `musan_music_10` | 3.6707 | 0.1483 | 4.128 | 3.447 |
| `musan_music_11` | 3.3297 | 2.8632 | 3.990 | 3.007 |
| `musan_music_12` | 4.0709 | 0.9132 | 4.583 | 3.821 |
| `musan_music_13` | 3.4864 | 0.3468 | 4.243 | 3.117 |
| `musan_music_14` | 3.1993 | 2.0309 | 4.147 | 2.736 |
| `musan_music_15` | 3.2193 | 0.7703 | 4.307 | 2.688 |
| `musan_music_16` | 3.8731 | 1.6359 | 4.404 | 3.614 |
| `musan_music_17` | 3.8407 | 3.3941 | 4.393 | 3.571 |
| `musan_music_18` | 3.9410 | 7.4425 | 4.140 | 3.844 |
| `musan_music_19` | 3.5585 | 3.4825 | 4.326 | 3.184 |
| `musan_music_20` | 3.7945 | 11.3142 | 4.413 | 3.493 |
