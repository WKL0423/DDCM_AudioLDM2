# AB shortlist (from budget report)

Use `ddcm_experiments/routeA_runs/.../ab_session/` as a template (see README_ab.txt).
Do not mix human scores with proxy CSVs; label files clearly.

## Budget <= 2560 bytes

| rank | source | run_dir_or_id |
| ---: | --- | --- |

## Budget <= 8192 bytes

| rank | source | run_dir_or_id |
| ---: | --- | --- |
| 1 | quality_push_large_codebook | `runs/T=20_in999-0_K=32_P=1_CB=3_model=audioldm2-music_audio` |
| 2 | ablation_step2 | `runs/T=20_in999-0_K=32_P=1_CB=3_model=audioldm2-music_audio` |
| 3 | quality_push_large_codebook | `runs/T=20_in999-0_K=32_P=2_CB=3_model=audioldm2-music_audio` |
| 4 | ablation_step2 | `runs/T=20_in999-0_K=32_P=2_CB=3_model=audioldm2-music_audio` |
| 5 | quality_push_large_codebook | `runs/T=10_in999-0_K=16_P=1_CB=3_model=audioldm2-music_audio` |

## Budget <= 20480 bytes

| rank | source | run_dir_or_id |
| ---: | --- | --- |
| 1 | quality_push_large_codebook | `runs/T=20_in999-0_K=32_P=1_CB=3_model=audioldm2-music_audio` |
| 2 | ablation_step2 | `runs/T=20_in999-0_K=32_P=1_CB=3_model=audioldm2-music_audio` |
| 3 | quality_push_large_codebook | `runs/T=20_in999-0_K=32_P=2_CB=3_model=audioldm2-music_audio` |
| 4 | ablation_step2 | `runs/T=20_in999-0_K=32_P=2_CB=3_model=audioldm2-music_audio` |
| 5 | quality_push_large_codebook | `runs/T=10_in999-0_K=16_P=1_CB=3_model=audioldm2-music_audio` |
