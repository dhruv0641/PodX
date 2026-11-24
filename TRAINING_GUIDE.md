# PodX — Audio Model Fine-Tuning Guide

This guide details the procedures, hardware prerequisites, and safety protocols for adapting speech models in PodX.

---

## 1. Architecture & Supported Methods

PodX supports parameter-efficient fine-tuning (PEFT) and Low-Rank Adaptation (LoRA) for audio speech synthesis models:
- **Target Architectures**: Qwen3-TTS 0.6B Base / CustomVoice, Kokoro acoustic adapters.
- **Adaptation Strategy**: Single-speaker LoRA per voice profile to avoid catastrophic acoustic drift.
- **Precision**: Mixed precision (FP16 / BF16) with gradient checkpointing.

---

## 2. Hardware Viability Guidelines

| Hardware Tier | Dedicated VRAM | System RAM | Supported Training Operation |
| :--- | :--- | :--- | :--- |
| **Entry (4 GB VRAM)** | 4,096 MB | 16 GB | LoRA rank $r=8$ on 0.6B models with batch size 1 and gradient accumulation. |
| **Studio (8 GB - 12 GB VRAM)** | 8,192 MB+ | 32 GB | Full LoRA rank $r=16/32$ with batch size 2–4. |
| **CPU-Only Fallback** | 0 MB | 16 GB - 32 GB | Offloaded training (high latency; recommended for small acoustic adapters only). |

---

## 3. Dataset Engineering Standards

Before uploading audio for fine-tuning:
1. **Sample Rate**: Audio must be clean 24 kHz or 48 kHz mono PCM.
2. **Signal-to-Noise Ratio (SNR)**: $> 25\text{ dB}$ (isolated from ambient reverb, HVAC noise, and background music).
3. **Slice Duration**: Slices must be segment-aligned between 3.0 and 15.0 seconds.
4. **Volume**: Normalized to -20 LUFS with no clipping.

---

## 4. Mandatory Consent & Ethics Protocols

PodX strictly forbids training models on unauthorized voice recordings:
- Every dataset registration requires explicit consent confirmation.
- Datasets must maintain provenance records documenting the recording source.
- Unauthorized voice cloning or impersonation of real individuals violates the acceptable use guidelines.
