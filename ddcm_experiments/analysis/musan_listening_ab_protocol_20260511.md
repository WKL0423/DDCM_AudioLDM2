# MUSAN subset listening — Pareto candidates (multi-listener)

Objective deltas between **`eta_late=0.30`** and **`0.35`** (both `@ eta_switch_t=200`) are small on MUSAN-20; this session checks **perceptual** preference on the same **7-clip** subset used in the eta sweep (3–5 hard + 2 easy).

## Prepared AB folder

| Item | Path |
|------|------|
| Session root | [runs/musan_ab_eta030_vs_eta035_sub7/ab_session](../../runs/musan_ab_eta030_vs_eta035_sub7/ab_session) |
| Hidden mapping | `ab_key.json` |
| Score template | `scores_template.csv` |
| Instructions | `README_ab.txt` |

**Clips:** `musan_music_01`, `03`, `05`, `17`, `18`, `19`, `20`.

**Source decodings:**

- Preset A (`eta_late_0.30`): rows in [musan_music_batch_metrics_20260506.json](../../runs/musan_music_batch_baseline_etaLate/musan_music_batch_metrics_20260506.json)
- Preset B (`eta_late_0.35`): [runs/musan_full_eta035_sw200_20260510/aggregate.json](../../runs/musan_full_eta035_sw200_20260510/aggregate.json)

Regenerate (e.g. new paths) with:

```bash
python tools/prepare_musan_ab_session.py \
  --aggregate-a runs/musan_music_batch_baseline_etaLate/musan_music_batch_metrics_20260506.json \
  --aggregate-b runs/musan_full_eta035_sw200_20260510/aggregate.json \
  --label-a eta_late_0.30_sw200 \
  --label-b eta_late_0.35_sw200 \
  --clip-ids musan_music_01,musan_music_03,musan_music_05,musan_music_17,musan_music_18,musan_music_19,musan_music_20 \
  --out-session runs/musan_ab_eta030_vs_eta035_sub7/ab_session \
  --seed 20260511
```

## Multi-listener protocol

1. Each listener copies `scores_template.csv` → `scores_listener_<name>.csv`.
2. For each trial: play `{trial_id}_reference.wav`, then `A` / `B`; choose closer to reference; fill `preferred_sample`, `confidence_1_to_5`, optional `notes`, `listener_id`.
3. **After** all trials, decode labels with `ab_key.json` and tally votes per preset (aggregate across listeners in a spreadsheet).

## Optional MOS columns

As noted in `README_ab.txt`, listeners may add `mos_A_1_to_5` and `mos_B_1_to_5` for absolute grades in addition to preference.

---

## Listening results (filled)

**Source:** [runs/musan_ab_eta030_vs_eta035_sub7/ab_session/scores_template.csv](../../runs/musan_ab_eta030_vs_eta035_sub7/ab_session/scores_template.csv) (single listener; `listener_id` left blank).

Decode with [ab_key.json](../../runs/musan_ab_eta030_vs_eta035_sub7/ab_session/ab_key.json): `A`/`B` map to `sample_A` / `sample_B` per trial.

| trial_id | clip | preferred | → preset | conf | notes |
|----------|------|-----------|----------|-----:|-------|
| trial1_musan_music_01 | musan_music_01 | A | **eta_late 0.30** | 3 | |
| trial2_musan_music_03 | musan_music_03 | B | **eta_late 0.30** | 3 | |
| trial3_musan_music_05 | musan_music_05 | B | **eta_late 0.30** | 4 | |
| trial4_musan_music_17 | musan_music_17 | B | **eta_late 0.35** | 4 | |
| trial5_musan_music_18 | musan_music_18 | B | **eta_late 0.30** | 5 | A and B almost same |
| trial6_musan_music_19 | musan_music_19 | A | **eta_late 0.30** | 5 | A and B almost same |
| trial7_musan_music_20 | musan_music_20 | A | **eta_late 0.35** | 1 | both poor on bass vs ref |

**Tally (7 trials):** **`eta_late=0.30` wins 5**, **`eta_late=0.35` wins 2** (clips `17` and `20`).

**Takeaway:** On this MUSAN hard/easy subset, **listening favors the lower late-η (0.30)** more often than the objective Pareto pick **0.35** from MUSAN-20 means. Treat **0.35** as an objective-driven option; **0.30** remains well supported for music preset choice when subjective alignment matters. Hard tails (`18`–`20`): listener still split **0.30** vs **0.35** on `17`/`20`, with low confidence on `20` and explicit bass complaint on both decodings.
