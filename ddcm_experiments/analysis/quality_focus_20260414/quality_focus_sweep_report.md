# Quality-Focused Sweep Report

## Baseline

- pearson_corr: 0.002593672
- mel_db_mae: 44.296875000
- snr_db: -8.308868799

## Top Candidates (piano, corr-primary)

| rank | source | name | corr | snr_db | mel_db_mae | bytes | delta_corr | delta_mel | delta_snr |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | quality_push_large_codebook | runs/T=120_in999-0_K=256_P=1_CB=3_model=audioldm | 0.036738 | -0.008837 | 8.015702 | 21768 | 0.034144 | -36.281173 | 8.300032 |
| 2 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=1_CB=3_model=audioldm2- | 0.011222 | -7.933532 | 38.681034 | 4645 | 0.008628 | -5.615841 | 0.375337 |
| 3 | ablation_step2 | runs/T=20_in999-0_K=32_P=1_CB=3_model=audioldm2- | 0.011222 | -7.933532 | 38.681034 | 4645 | 0.008628 | -5.615841 | 0.375337 |
| 4 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=2_CB=3_model=audioldm2- | 0.006877 | -9.543597 | 34.788227 | 5556 | 0.004283 | -9.508648 | -1.234728 |
| 5 | ablation_step2 | runs/T=20_in999-0_K=32_P=2_CB=3_model=audioldm2- | 0.006877 | -9.543597 | 34.788227 | 5556 | 0.004283 | -9.508648 | -1.234728 |

## Top with known bitstream size (inferred or explicit)

| rank | source | name | corr | bytes |
| --- | --- | --- | ---: | ---: |
| 1 | quality_push_large_codebook | runs/T=120_in999-0_K=256_P=1_CB=3_model=audioldm | 0.036738 | 21768 |
| 2 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=1_CB=3_model=audioldm2- | 0.011222 | 4645 |
| 3 | ablation_step2 | runs/T=20_in999-0_K=32_P=1_CB=3_model=audioldm2- | 0.011222 | 4645 |
| 4 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=2_CB=3_model=audioldm2- | 0.006877 | 5556 |
| 5 | ablation_step2 | runs/T=20_in999-0_K=32_P=2_CB=3_model=audioldm2- | 0.006877 | 5556 |

## Recommendation

- Recommended candidate: `runs/T=120_in999-0_K=256_P=1_CB=3_model=audioldm2-music_audio` from `quality_push_large_codebook` (payload bytes=21768).
- Prefer tuning from candidates with known positive payload when comparing rate.

## Mel-first ranking (piano, known payload)

| rank | mel_db_mae | snr_db | corr | bytes | json | bin | source | name |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | 6.1953 | -0.3302 | -0.0549 | 14838 | 14768 | 70 | quality_push_large_codebook | runs/T=80_in999-0_K=128_P=1_CB=3_model=a |
| 2 | 7.9262 | -0.0846 | -0.0255 | 44586 | 44386 | 200 | quality_push_large_codebook | runs/T=200_in999-0_K=256_P=2_CB=3_model= |
| 3 | 7.9399 | -0.1317 | -0.0726 | 173082 | 171833 | 1249 | quality_push_large_codebook | runs/T=999_in999-0_K=1000_P=1_CB=3_model |
| 4 | 7.9517 | -0.2291 | -0.1799 | 35390 | 35190 | 200 | quality_push_large_codebook | runs/T=200_in999-0_K=256_P=1_CB=3_model= |
| 5 | 8.0157 | -0.0088 | 0.0367 | 21768 | 21648 | 120 | quality_push_large_codebook | runs/T=120_in999-0_K=256_P=1_CB=3_model= |
| 6 | 34.7882 | -9.5436 | 0.0069 | 5556 | 5543 | 13 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=2_CB=3_model=au |
| 7 | 34.7882 | -9.5436 | 0.0069 | 5556 | 5543 | 13 | ablation_step2 | runs/T=20_in999-0_K=32_P=2_CB=3_model=au |
| 8 | 38.6810 | -7.9335 | 0.0112 | 4645 | 4632 | 13 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=1_CB=3_model=au |
| 9 | 38.6810 | -7.9335 | 0.0112 | 4645 | 4632 | 13 | ablation_step2 | runs/T=20_in999-0_K=32_P=1_CB=3_model=au |
| 10 | 44.0378 | -7.9549 | -0.0022 | 3414 | 3409 | 5 | quality_push_large_codebook | runs/T=10_in999-0_K=16_P=2_CB=3_model=au |

## Pareto frontier (piano): minimize bytes and mel_db_mae

| mel_db_mae | bytes | json | bin | corr | source | name |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 44.2969 | 2971 | 2966 | 5 | 0.0026 | quality_push_large_codebook | runs/T=10_in999-0_K=16_P=1_CB=3_model=au |
| 44.2969 | 2971 | 2966 | 5 | 0.0026 | ablation_step2 | runs/T=10_in999-0_K=16_P=1_CB=3_model=au |
| 44.0378 | 3414 | 3409 | 5 | -0.0022 | quality_push_large_codebook | runs/T=10_in999-0_K=16_P=2_CB=3_model=au |
| 44.0378 | 3414 | 3409 | 5 | -0.0022 | ablation_step2 | runs/T=10_in999-0_K=16_P=2_CB=3_model=au |
| 38.6810 | 4645 | 4632 | 13 | 0.0112 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=1_CB=3_model=au |
| 38.6810 | 4645 | 4632 | 13 | 0.0112 | ablation_step2 | runs/T=20_in999-0_K=32_P=1_CB=3_model=au |
| 34.7882 | 5556 | 5543 | 13 | 0.0069 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=2_CB=3_model=au |
| 34.7882 | 5556 | 5543 | 13 | 0.0069 | ablation_step2 | runs/T=20_in999-0_K=32_P=2_CB=3_model=au |
| 6.1953 | 14838 | 14768 | 70 | -0.0549 | quality_push_large_codebook | runs/T=80_in999-0_K=128_P=1_CB=3_model=a |

## Non-piano material probe (not mixed into primary recommendation)

| stem | mel_db_mae | snr_db | corr | bytes | json | bin | source | name |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| techno_music_with_beats | 4.0724 | -1.4673 | 0.1130 | 172208 | 170959 | 1249 | quality_push_large_codebook | runs/T=999_in999-0_K=1000_P=1_CB |
| techno_music_with_beats | 5.8439 | -1.3697 | 0.0198 | 21618 | 21498 | 120 | quality_push_large_codebook | runs/T=120_in999-0_K=256_P=1_CB= |
| techno_music_with_beats | 7.4179 | -2.1269 | 0.0244 | 14838 | 14768 | 70 | quality_push_large_codebook | runs/T=80_in999-0_K=128_P=1_CB=3 |
| techno_music_with_beats | 10.9270 | -2.3183 | 0.0042 | 4679 | 4666 | 13 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=1_CB=3_ |
| synth_pinkish_12s | 11.2407 | -3.2840 | -0.0012 | 4672 | 4659 | 13 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=1_CB=3_ |
| synth_chirp_15s | 33.9700 | -1.4825 | 0.0021 | 4643 | 4630 | 13 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=1_CB=3_ |
| synth_amclick_14s | 37.3896 | -5.8310 | -0.0129 | 4638 | 4625 | 13 | quality_push_large_codebook | runs/T=20_in999-0_K=32_P=1_CB=3_ |
