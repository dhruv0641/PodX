---
name: audio-quality-evaluation
description: Autonomous ASR verification, WER/CER auditing, and acoustic anomaly detection.
---

# Audio Quality Evaluation Skill

## Purpose
Verifies the synthesized audio matches the original script with zero hallucinations, omissions, or audio glitches.

## Quality Checks
1. **Whisper ASR Alignment**: Transcribe generated audio with local Faster-Whisper / Whisper and compute Word Error Rate (WER).
2. **Clipping & Distortion**: Detect sample values exceeding 0.999 (-0.01 dBFS).
3. **Excessive Silence**: Alert if silence blocks exceed 3.0 continuous seconds without a script pause instruction.
4. **Hallucination Detection**: Flag synthesized tokens not present in source sentence.
5. **Bounded Retries**: Defective segments trigger up to 2 retries with adjusted temperature/seed before human review flag.

