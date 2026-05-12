# Phase 1 budget report

- Candidates with known payload (piano only): **13** / 13 piano (unknown: 0); non-piano rows excluded: **7**

## Baseline (step1 piano metrics file)

- pearson_corr=0.002594, mel_db_mae=44.296875, snr_db=-8.308869

## Budget <= 2560 bytes (0 shown, top 5)

| rank | bytes | corr | mel_db_mae | snr_db | source | name |
| ---:| ---:| ---:| ---:| ---:| --- | --- |

## Budget <= 8192 bytes (5 shown, top 5)

| rank | bytes | corr | mel_db_mae | snr_db | source | name |
| ---:| ---:| ---:| ---:| ---:| --- | --- |
| 1 | 4645 | 0.01122 | 38.68103 | -7.93353 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=1_CB=3_model=audioldm2-music_au |
| 2 | 4645 | 0.01122 | 38.68103 | -7.93353 | ablation_step2 | runs/T=20_in999-0_K=32_P=1_CB=3_model=audioldm2-music_au |
| 3 | 5556 | 0.00688 | 34.78823 | -9.54360 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=2_CB=3_model=audioldm2-music_au |
| 4 | 5556 | 0.00688 | 34.78823 | -9.54360 | ablation_step2 | runs/T=20_in999-0_K=32_P=2_CB=3_model=audioldm2-music_au |
| 5 | 2971 | 0.00259 | 44.29688 | -8.30887 | quality_push_large_codebook | runs/T=10_in999-0_K=16_P=1_CB=3_model=audioldm2-music_au |

## Budget <= 20480 bytes (5 shown, top 5)

| rank | bytes | corr | mel_db_mae | snr_db | source | name |
| ---:| ---:| ---:| ---:| ---:| --- | --- |
| 1 | 4645 | 0.01122 | 38.68103 | -7.93353 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=1_CB=3_model=audioldm2-music_au |
| 2 | 4645 | 0.01122 | 38.68103 | -7.93353 | ablation_step2 | runs/T=20_in999-0_K=32_P=1_CB=3_model=audioldm2-music_au |
| 3 | 5556 | 0.00688 | 34.78823 | -9.54360 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=2_CB=3_model=audioldm2-music_au |
| 4 | 5556 | 0.00688 | 34.78823 | -9.54360 | ablation_step2 | runs/T=20_in999-0_K=32_P=2_CB=3_model=audioldm2-music_au |
| 5 | 2971 | 0.00259 | 44.29688 | -8.30887 | quality_push_large_codebook | runs/T=10_in999-0_K=16_P=1_CB=3_model=audioldm2-music_au |

