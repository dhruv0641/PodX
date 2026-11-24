---
name: audio-mastering
description: Broadcast-grade audio post-production and mastering pipeline.
---

# Audio Mastering Skill

## Purpose
Transforms raw synthesized speech chunks into broadcast-quality audio adhering to international podcasting standards.

## Production Specifications
1. **Loudness Standards**: Integrated loudness targeted at -16.0 LUFS for stereo (-19.0 LUFS for mono) +/- 0.5 LUFS.
2. **True Peak Ceiling**: Limited to -1.0 dBTP to prevent inter-sample distortion across MP3/AAC encoders.
3. **Signal Chain**:
   - High-pass filtering at 80 Hz (cuts mic rumble and DC offset).
   - De-essing at 5.5 kHz - 7.5 kHz (attenuates harsh sibilance).
   - Gentle dynamic range compression (2:1 to 3:1 ratio, 20ms attack, 100ms release).
   - Parametric warming (+1.5 dB around 200 Hz).
   - Limiting / Normalization.
   - Ducking: Lowers background bed audio by 12-16 dB whenever dialogue is active.

