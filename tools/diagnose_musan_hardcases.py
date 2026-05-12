#!/usr/bin/env python3
"""Spectral / energy diagnostics for MUSAN ref vs DDCM decomp (hard-case triage)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import soundfile as sf


def load_mono(path: Path, sr_target: int) -> tuple[np.ndarray, int]:
    x, sr = sf.read(str(path), always_2d=True)
    x = x.astype(np.float32).mean(axis=1)
    if sr != sr_target:
        import math

        ratio = sr_target / sr
        n_out = max(1, int(round(len(x) * ratio)))
        xi = np.linspace(0.0, len(x) - 1, num=len(x), dtype=np.float32)
        xo = np.linspace(0.0, len(x) - 1, num=n_out, dtype=np.float32)
        x = np.interp(xo, xi, x).astype(np.float32)
        sr = sr_target
    return x, sr


def frame_rms(x: np.ndarray, frame: int, hop: int) -> np.ndarray:
    n = 1 + (len(x) - frame) // hop if len(x) >= frame else 0
    if n <= 0:
        return np.array([], dtype=np.float32)
    out = np.empty(n, dtype=np.float32)
    for i in range(n):
        sl = x[i * hop : i * hop + frame]
        out[i] = float(np.sqrt(np.mean(sl * sl) + 1e-12))
    return out


def mel_like_energy(x: np.ndarray, sr: int, n_fft: int, hop: int, n_mels: int) -> np.ndarray:
    """Cheap mel-band energy (no librosa): STFT magnitude * triangular mel weights."""
    # Hann STFT
    n = len(x)
    n_frames = 1 + (n - n_fft) // hop if n >= n_fft else 0
    if n_frames <= 0:
        return np.zeros((n_mels, 0), dtype=np.float32)
    win = np.hanning(n_fft).astype(np.float32)
    spec = np.zeros((n_fft // 2 + 1, n_frames), dtype=np.float32)
    for t in range(n_frames):
        sl = x[t * hop : t * hop + n_fft] * win
        sp = np.fft.rfft(sl)
        spec[:, t] = np.abs(sp).astype(np.float32)
    # Mel bin edges (HTK-like): linear low, log high — simplified uniform in mel
    def hz_to_mel(f):
        return 2595.0 * np.log10(1.0 + f / 700.0)

    def mel_to_hz(m):
        return 700.0 * (10.0 ** (m / 2595.0) - 1.0)

    mel_lo, mel_hi = hz_to_mel(0.0), hz_to_mel(sr / 2.0)
    mels = np.linspace(mel_lo, mel_hi, n_mels + 2)
    hz = mel_to_hz(mels).astype(np.float32)
    bins = np.linspace(0.0, sr / 2.0, spec.shape[0], dtype=np.float32)
    fb = np.zeros((n_mels, spec.shape[0]), dtype=np.float32)
    for m in range(n_mels):
        f_lo, f_c, f_hi = hz[m], hz[m + 1], hz[m + 2]
        rising = (bins - f_lo) / max(f_c - f_lo, 1e-6)
        falling = (f_hi - bins) / max(f_hi - f_c, 1e-6)
        tri = np.maximum(0.0, np.minimum(rising, falling))
        fb[m] = tri / (tri.sum() + 1e-12)
    mel = fb @ spec
    mel_db = 10.0 * np.log10(mel + 1e-10)
    return mel_db


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics-json", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--sr", type=int, default=16000)
    ap.add_argument("--plot", action="store_true", help="Write PNG plots (needs matplotlib)")
    args = ap.parse_args()

    metrics = json.loads(args.metrics_json.read_text(encoding="utf-8"))
    rows = metrics["rows"]
    args.out_dir.mkdir(parents=True, exist_ok=True)

    if args.plot:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

    summary = []

    for row in rows:
        aid = row["audio"]
        ref_p = Path(row["input_path"])
        out_dir = Path(row["out_dir"])
        stem = ref_p.stem
        dec_p = out_dir / f"{stem}_decomp.wav"
        if not dec_p.exists():
            summary.append({"audio": aid, "error": f"missing {dec_p}"})
            continue

        ref, sr = load_mono(ref_p, args.sr)
        dec, _ = load_mono(dec_p, args.sr)
        n = min(len(ref), len(dec))
        ref, dec = ref[:n], dec[:n]

        rms_ref = frame_rms(ref, 1024, 256)
        rms_dec = frame_rms(dec, 1024, 256)
        m = min(len(rms_ref), len(rms_dec))
        rms_ref, rms_dec = rms_ref[:m], rms_dec[:m]
        env_l1 = float(np.mean(np.abs(rms_ref - rms_dec)))

        mel_r = mel_like_energy(ref, sr, 1024, 256, 64)
        mel_d = mel_like_energy(dec, sr, 1024, 256, 64)
        f = min(mel_r.shape[1], mel_d.shape[1])
        mel_r, mel_d = mel_r[:, :f], mel_d[:, :f]
        mel_mae = float(np.mean(np.abs(mel_r - mel_d)))
        # band split: low bins 0-15 vs rest
        low_mae = float(np.mean(np.abs(mel_r[:16] - mel_d[:16])))
        high_mae = float(np.mean(np.abs(mel_r[16:] - mel_d[16:])))

        # crude failure tag
        tags = []
        if row.get("stft_mag_mse", 0) > 3.0:
            tags.append("high_stft_tail")
        if row.get("mel_db_mae", 0) > 4.5:
            tags.append("high_mel_mae")
        if high_mae > low_mae * 1.25:
            tags.append("hf_heavy_mismatch")
        elif low_mae > high_mae * 1.25:
            tags.append("lf_heavy_mismatch")
        else:
            tags.append("broadband_mismatch")
        if env_l1 > 0.02:
            tags.append("envelope_drift")

        rec = {
            "audio": aid,
            "mel_db_mae_table": row.get("mel_db_mae"),
            "stft_mag_mse_table": row.get("stft_mag_mse"),
            "envelope_rms_l1": env_l1,
            "mel_proxy_mae_db": mel_mae,
            "mel_proxy_low_mae": low_mae,
            "mel_proxy_high_mae": high_mae,
            "failure_tags": tags,
        }
        summary.append(rec)

        if args.plot:
            fig, axs = plt.subplots(3, 1, figsize=(10, 8), constrained_layout=True)
            t = np.arange(n) / sr
            axs[0].plot(t, ref, lw=0.3, label="ref")
            axs[0].plot(t, dec, lw=0.3, alpha=0.7, label="decomp")
            axs[0].set_title(f"{aid} waveform")
            axs[0].legend(loc="upper right")

            tt = np.arange(m) * 256 / sr
            axs[1].plot(tt, rms_ref, label="rms ref")
            axs[1].plot(tt, rms_dec, alpha=0.7, label="rms decomp")
            axs[1].set_title("Frame RMS envelope")
            axs[1].legend()

            diff = mel_r - mel_d
            im = axs[2].imshow(diff, aspect="auto", origin="lower", cmap="coolwarm", vmin=-6, vmax=6)
            axs[2].set_title("Mel-like (dB) difference (ref - decomp)")
            fig.colorbar(im, ax=axs[2], fraction=0.02)
            fig.savefig(args.out_dir / f"{aid}_diag.png", dpi=120)
            plt.close(fig)

    (args.out_dir / "hardcase_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = ["# MUSAN hard-case diagnostic summary\n"]
    for s in summary:
        lines.append(f"## {s.get('audio', '?')}\n")
        if "error" in s:
            lines.append(f"- error: {s['error']}\n")
            continue
        lines.append(f"- table `mel_db_mae`: {s['mel_db_mae_table']:.4f}\n")
        lines.append(f"- table `stft_mag_mse`: {s['stft_mag_mse_table']:.4f}\n")
        lines.append(f"- envelope RMS L1 (frame): {s['envelope_rms_l1']:.5f}\n")
        lines.append(f"- mel-proxy MAE (dB): {s['mel_proxy_mae_db']:.4f} (low {s['mel_proxy_low_mae']:.4f}, high {s['mel_proxy_high_mae']:.4f})\n")
        lines.append(f"- **tags**: {', '.join(s['failure_tags'])}\n")
    (args.out_dir / "hardcase_summary.md").write_text("".join(lines), encoding="utf-8")
    print("Wrote", args.out_dir / "hardcase_summary.md")


if __name__ == "__main__":
    main()
