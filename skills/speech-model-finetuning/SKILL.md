---
name: speech-model-finetuning
description: LoRA and PEFT fine-tuning pipeline for voice adaptation and customization.
---

# Speech Model Fine-Tuning Skill

## Purpose
Enables fine-tuning audio TTS models (e.g. Qwen3-TTS, Kokoro adapters) on user-provided, consented voice datasets.

## Pipeline Steps
1. **Provenance & Consent**: Reject datasets lacking verified consent or attribution.
2. **Data Cleansing**: Resample to target rate (24kHz), trim silence using VAD, filter audio with SNR < 20 dB.
3. **Alignment**: Align transcripts to audio chunks (3-15 seconds per slice).
4. **Training Loop**: Execute PEFT/LoRA training with gradient accumulation, mixed precision (fp16), and memory monitoring.
5. **Checkpoint Validation**: Generate evaluation sentences on each epoch; compute loss curve and save weights.

