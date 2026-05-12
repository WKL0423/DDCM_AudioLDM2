# MUSAN failure-mode triage (phase 1)

Artifacts: PNG + JSON from [tools/diagnose_musan_hardcases.py](../../tools/diagnose_musan_hardcases.py) → `runs/musan_hardcase_diag_20260510/`.

## Four coarse failure families (for phase-2 sweeps)

1. **STFT-tail / transient-heavy** (`high_stft_tail`): strong wideband spectral mismatch while `mel_db_mae` stays moderate. Seen on `musan_music_17–20`, often with **envelope_drift** (frame-RMS mismatch). *Hypothesis*: broadband energy or transient smear not captured by 128-bin torchaudio mel alone.
2. **Mel–STFT disagreement** (`musan_music_03`): **very low** `stft_mag_mse` but **highest** `mel_db_mae`; envelope RMS almost unchanged. *Hypothesis*: fine mel texture / masking differences rather than gross STFT energy; worth `score-mode-late` / mel-proxy style knobs before touching `K`.
3. **High mel + moderate STFT** (`musan_music_04`): both metrics elevated, broadband tag. *Hypothesis*: mixed timbre + spectral tilt; treat as general “hard clip”.
4. **Easy / stable** (`musan_music_05`, `01`): low `mel_db_mae`, low `stft_mag_mse`, small envelope error — use as **regression guards** in sweeps.

## Sweep guidance (phase 2)

- Prioritize **eta schedule** and **`eta_switch_t`** on clips in family (1) and the outlier (2).
- Keep **`musan_music_05` + `musan_music_01`** in every sweep row to catch regressions.
