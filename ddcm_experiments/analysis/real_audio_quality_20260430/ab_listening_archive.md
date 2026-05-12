# Guanyu AB listening — archive (phase 0)

## Scope

Two prepared AB sessions for `theme_of_guanyu_16k.wav`:

| Session | Directory | Trials |
|--------|-----------|--------|
| Config comparison (baseline / P2 / K2000P1) | [runs/real_audio_guanyu_ab_20260430/ab_session](../../../runs/real_audio_guanyu_ab_20260430/ab_session) | `trial1_baseline_vs_p2`, `trial2_baseline_vs_k2000p1`, `trial3_p2_vs_k2000p1` |
| Strategy follow-up (baseline / eta-late / blend) | [runs/real_audio_guanyu_ab_20260430_etaLate/ab_session](../../../runs/real_audio_guanyu_ab_20260430_etaLate/ab_session) | `trial1_baseline_vs_etaLate`, `trial2_etaLate_vs_blend`, `trial3_baseline_vs_blend` |

Each folder contains `reference_original.wav`, paired `trial*_A/B.wav`, `ab_key.json`, `scores_template.csv`, and `README_ab.txt` (eta-late folder).

## Subjective scores status (server copy)

**Filled** (listener `preferred_sample` / `confidence` present) in:

- [runs/real_audio_guanyu_ab_20260430/ab_session/scores_template.csv](../../../runs/real_audio_guanyu_ab_20260430/ab_session/scores_template.csv)
- [runs/real_audio_guanyu_ab_20260430_etaLate/ab_session/scores_template.csv](../../../runs/real_audio_guanyu_ab_20260430_etaLate/ab_session/scores_template.csv)

Decode with each folder’s `ab_key.json` (after scoring).

### Session A — config (`real_audio_guanyu_ab_20260430`)

| trial | Preferred | Maps to (see `ab_key.json`) |
|-------|-----------|------------------------------|
| trial1_baseline_vs_p2 | B | **T999_K1000_P2** over T999_K1000_P1 |
| trial2_baseline_vs_k2000p1 | B | **T999_K2000_P1** over T999_K1000_P1 |
| trial3_p2_vs_k2000p1 | B | **T999_K2000_P1** over T999_K1000_P2 (head-to-head) |

All trials: confidence **3**; `notes` left empty.

### Session B — strategy (`real_audio_guanyu_ab_20260430_etaLate`)

| trial | Preferred | Maps to |
|-------|-----------|---------|
| trial1_baseline_vs_etaLate | A | **T999_K1000_P2 (no eta-late)** over `ETA 1.0→0.3 @ t≤200` |
| trial2_etaLate_vs_blend | A | **eta-late** over blend+eta-late |
| trial3_baseline_vs_blend | A | **T999_K1000_P2 (no eta-late)** over blend+eta-late |

Confidences **2** (low–moderate); `notes` empty.

## Preset decision (after subjective sheets)

**Listening on `theme_of_guanyu_16k.wav` does not support elevating eta-late to the official default:** session B trial1 prefers **plain `T999_K1000_P2`** over eta-late. Ordering among strategies is consistent with **baseline (no eta-late) > eta-late > full blend+eta-late** on these trials.

Session A is **mixed vs objective ranking:** listener prefers **T999_K2000_P1** over **T999_K1000_P2** in direct AB (trial3), while still preferring P2 and K2000P1 each over T999_K1000_P1. Treat **Guanyu** as a single-track tie-break hint only; batch MUSAN/SQAM presets may still follow objective + separate AB.

**Subjective-first default for this listener on Guanyu:** emphasize **`T999_K1000_P2` without eta-late** for parity with trial1; if config must move off P2 on this clip, **`T999_K2000_P1`** was preferred over P2 head-to-head.

**Objective / engineering default** (unchanged for large-scale sweeps): many runs still use **`T999_K1000_P2 + eta_late(1.0→0.3 @ 200)`** or the newer **`eta_late=0.35`** candidate from MUSAN — document which population each preset targets.

**Rationale on record:** objective metrics favored P2 and eta-late; subjective Guanyu AB partially disagrees (no eta-late; K2000P1 over P2). Keep both logs when writing papers or product defaults.

## Listener checklist (when you run the AB)

1. Calibrate level-matched playback if possible (same peak or LUFS).
2. For each trial, prefer the sample closer to **reference** in timbre, musical noise, and absence of warble/metallic artifacts.
3. Record `preferred_sample` as `A` or `B`, `confidence_1_to_5`, and short `notes`.
4. After scoring, compare your choices against `ab_key.json` only if you want to map to algorithm labels; keep blind scoring until finished.
