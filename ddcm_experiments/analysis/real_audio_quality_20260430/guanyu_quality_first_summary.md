# Real Audio Quality-First Summary (2026-04-30)

## Input and policy
- Input track: `theme_of_guanyu_16k.wav` (from uploaded `Theme of Guanyu.mp3`).
- Policy: quality-first selection (payload is recorded but not used for ranking).
- Fixed settings across sweep: `model=cvssp/audioldm2-music`, `t_range=999->0`, `coef_bits=4`.

## Tested configs
- Baselines:
  - `T120_K256_P1`
  - `T999_K1000_P1`
- Quality sweep:
  - `T999_K2000_P1`
  - `T999_K1000_P2`
  - `T999_K2000_P2`

## Objective ranking rule
- Primary ranking: `mel_db_mae` (lower), then `stft_mag_mse` (lower).
- Tie/support: `final_latent_cosine` (higher), `final_latent_rel_l2` (lower).
- `snr_db` / `pearson_corr` are reference-only.

## Objective results snapshot

| config | mel_db_mae | stft_mag_mse | final_latent_cosine | final_latent_rel_l2 | snr_db | pearson_corr |
|:--|--:|--:|--:|--:|--:|--:|
| T999_K1000_P2 | 3.9039 | 0.3069 | 0.9587 | 0.2878 | -3.0939 | -0.0522 |
| T999_K2000_P1 | 4.0409 | 0.3410 | 0.9512 | 0.3124 | -2.7256 | -0.0296 |
| T999_K2000_P2 | 4.1315 | 0.3200 | 0.9612 | 0.2785 | -3.2675 | -0.0721 |
| T999_K1000_P1 | 4.2171 | 0.3410 | 0.9487 | 0.3203 | -2.9071 | -0.0404 |
| T120_K256_P1  | 5.7472 | 0.5941 | 0.8679 | 0.4993 | -1.5166 | 0.0472 |

Raw machine-readable results:
- `runs/real_audio_guanyu_quality_sweep_20260430.json`

## AB package prepared
- Folder: `runs/real_audio_guanyu_ab_20260430/ab_session`
- Includes:
  - `reference_original.wav`
  - 3 randomized pairwise trials:
    - baseline vs P2
    - baseline vs K2000P1
    - P2 vs K2000P1
  - `scores_template.csv`
  - hidden mapping: `ab_key.json`
  - quick instructions: `README_ab.txt`

## Frozen preset (quality-first working default)
- **Working default preset:** `T999_K1000_P2`
- Why:
  - best `mel_db_mae`
  - best `stft_mag_mse`
  - strongest latent alignment among top performers
- Note:
  - this is a quality-first default now;
  - finalize as the official preset after human AB sheet (`scores_template.csv`) is filled.

## Strategy refinement (eta-late)
- Additional strategy sweep file:
  - `runs/real_audio_guanyu_strategy_sweep_20260430.json`
- Compared against baseline `T999_K1000_P2`, three variants were tested:
  - blend-to-cosine score switch
  - eta-late schedule (`ETA=1.0 -> 0.3 @ t<=200`)
  - blend + eta-late
- Best objective variant in this sweep: **eta-late**.
  - baseline: `mel_db_mae=3.9039`, `stft_mag_mse=0.3069`
  - eta-late: `mel_db_mae=3.8556`, `stft_mag_mse=0.2910`
- Updated working default preset (quality-first):
  - **`T999_K1000_P2 + ETA=1.0->0.3 @ t<=200`**

## Follow-up AB package (eta-late vs baseline)
- Folder: `runs/real_audio_guanyu_ab_20260430_etaLate/ab_session`
- Includes:
  - `reference_original.wav`
  - `trial1_baseline_vs_etaLate_A/B.wav`
  - `trial2_etaLate_vs_blend_A/B.wav`
  - `trial3_baseline_vs_blend_A/B.wav`
  - `scores_template.csv` and hidden mapping `ab_key.json`

## Next action for listener

Done: both `scores_template.csv` copies are filled; see [ab_listening_archive.md](ab_listening_archive.md) for decode and implications.

## AB archive status (after subjective fill)

- **`scores_template.csv` is filled** in both [runs/real_audio_guanyu_ab_20260430/ab_session](../../runs/real_audio_guanyu_ab_20260430/ab_session) and [runs/real_audio_guanyu_ab_20260430_etaLate/ab_session](../../runs/real_audio_guanyu_ab_20260430_etaLate/ab_session). Full trial table: [ab_listening_archive.md](ab_listening_archive.md).
- **Guanyu listening:** listener prefers **`T999_K1000_P2` without eta-late** over eta-late (strategy session); head-to-head config session prefers **`T999_K2000_P1`** over **`T999_K1000_P2`**. Confidences 2–3.
- **Batch / objective line** may still use **`T999_K1000_P2 + eta_late`** (e.g. MUSAN tuning); label presets as **objective-optimized** vs **Guanyu-subjective** where they differ.

