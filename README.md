# DDCM × AudioLDM2

在 **AudioLDM2（diffusers）** 上实现 DDCM 相关编解码与批量评测的代码库。训练侧上游工程请单独克隆（见 `.gitignore` 中的说明），本仓库保留**可复现实验**所需的脚本、核心库与**文字类试验记录**。

## 依赖与环境

| 说明 | 路径 |
|------|------|
| Python 依赖清单（与 Docker 基础镜像配合；不含 PyTorch 本体时见各 Dockerfile） | `requirements-core.txt` |
| Windows / Conda 逐步安装与 HF 缓存 | `SETUP_NEW_MACHINE.md` |
| Docker 构建与运行 | `README_DOCKER.md`、`Dockerfile.cpu`、`Dockerfile.cuda`、`docker-compose.yml` |
| 新机器 PowerShell 辅助脚本 | `scripts/setup_new_machine.ps1` |

建议：设置 `HF_HOME` 或 `HUGGINGFACE_HUB_CACHE`，避免重复下载 `cvssp/audioldm2-music` 等权重。

## 最小跑通检查

在已安装 PyTorch、diffusers、transformers 等依赖的环境中：

```bash
python smoke_test_sampler.py --help
python main.py
```

（`main.py` 会按默认提示词生成短音频到当前目录，需 GPU/显存与模型缓存。）

## 核心实验入口

- **DDCM 步进编解码**：`step2b_ddcm_step_encode.py`、`step3b_ddcm_step_decode.py`；整段流程见 `step2_ddcm_compress_audio.py` / `step3_ddcm_decompress_audio.py`。
- **通用压缩入口**：`audio_compression.py`（被子进程或脚本调用）。
- **批量 roundtrip + 指标**：`tools/run_batch_roundtrip.py`（可用环境变量 `DDCM_PYTHON` 指定解释器）。
- **子集 η 扫描**：`tools/run_subset_eta_sweep.py`。
- **MUSAN AB 材料准备**：`tools/prepare_musan_ab_session.py`。
- **指标与诊断**：`tools/compare_audio_metrics.py`、`tools/diagnose_musan_hardcases.py` 等。

数据与大规模输出默认**不提交**：`datasets/`、`runs/` 在 `.gitignore` 中；请本地准备 manifest 指向的 wav，并将 `runs/` 作为实验输出目录。

## 关键试验记录（文本）

- **汇总与分析（推荐同步到 Git）**：`ddcm_experiments/analysis/`  
  含 MUSAN/SQAM 批报告、η 扫描摘要、AB 协议、硬例分析等 Markdown/小 JSON。
- **质量协议与一页纸**：`ddcm_experiments/EVAL_PROTOCOL_QUALITY_FIRST.md`、`ddcm_experiments/REPORT_ONEPAGE_QUALITY_FIRST.md`。
- **基线包说明**：`ddcm_experiments/baselines/latent_fixed_20260414/`。
- **Step1 基线笔记**：`STEP1_BASELINE_REPORT.md`。
- **变更备忘**：`CHANGELOG_PLAN_A.md`、`memo.md`。

听感 AB 的 wav 体积大，仍由 `.gitignore` 中的 `*.wav` 等规则排除；仓库内保留**协议与数字结果**，波形放在本地 `runs/.../ab_session/` 即可。
