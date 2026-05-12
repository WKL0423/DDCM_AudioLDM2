# Test coverage plan — implementation index (2026-05-11)

Deliverables from the optional todos in the test-coverage assessment.

| Todo | What was added |
|------|----------------|
| Unified reports | [tools/render_batch_aggregate_report.py](../../tools/render_batch_aggregate_report.py); [tools/run_batch_roundtrip.py](../../tools/run_batch_roundtrip.py) flags `--aggregate-md` / `--aggregate-md-title`. Examples: [batch_report_musan_full_eta035_20260510.md](batch_report_musan_full_eta035_20260510.md), [batch_report_sqam_full_eta035_20260510.md](batch_report_sqam_full_eta035_20260510.md). |
| Extended benchmark | [tools/build_musan_music_extend_manifest.py](../../tools/build_musan_music_extend_manifest.py) → [datasets/musan_music_16k_extend12/manifest.json](../../datasets/musan_music_16k_extend12/manifest.json); baseline run [runs/musan_extend12_baseline_eta030_20260511/aggregate.json](../../runs/musan_extend12_baseline_eta030_20260511/aggregate.json); alignment note [musan_extend12_baseline_alignment_20260511.md](musan_extend12_baseline_alignment_20260511.md). |
| MUSAN listening | [tools/prepare_musan_ab_session.py](../../tools/prepare_musan_ab_session.py); session [runs/musan_ab_eta030_vs_eta035_sub7/ab_session](../../runs/musan_ab_eta030_vs_eta035_sub7/ab_session); protocol + **filled decode** [musan_listening_ab_protocol_20260511.md](musan_listening_ab_protocol_20260511.md) (**5×0.30** vs **2×0.35** on 7 clips). |
| Stable Audio phase 1 (isolated) | [stable_audio_lab/README.md](../../stable_audio_lab/README.md), [stable_audio_lab/requirements.txt](../../stable_audio_lab/requirements.txt), [stable_audio_lab/scripts/smoke_generate.py](../../stable_audio_lab/scripts/smoke_generate.py); outputs under [runs_stable_audio/](../../runs_stable_audio/) (gitignored). |
