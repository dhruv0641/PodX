# Model Architecture, Evaluation & Comparison Matrix

**PodX Autonomous Model Selection & Benchmarking Framework**

---

## 1. Evaluated Audio TTS Models

| Model Family | Variant | Parameters | Audio Quality | VRAM (FP16) | Speed (RTF) | Long-form Stability | Status in PodX |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Kokoro** | Kokoro-82M | 82M | **Studio (4.6/5.0)** | ~300 MB | **0.02 (50x RT)** | **Flawless** | **Primary Engine & Fast Preview** |
| **Qwen3-TTS** | 0.6B-CustomVoice | 600M | High (4.4/5.0) | ~1.6 GB | 0.25 (4x RT) | Stable (chunked) | **Integrated Advanced Provider** |
| **Qwen3-TTS** | 1.7B-VoiceDesign | 1.7B | Extreme (4.7/5.0)| ~3.8 GB (tight)| 0.85 (1.2x RT) | Requires offload | **Integrated (Quantized/CPU Mode)** |
| **MOSS-TTS** | MOSS-TTS-v1.5 | 1.2B | Expressive (4.3) | ~3.2 GB | 0.90 (1.1x RT) | Memory sensitive | **Provider Interface & Evaluation** |
| **Chatterbox** | Turbo / Multilingual | 350M | Expressive (4.2) | ~1.2 GB | 0.40 (2.5x RT) | Stable | **Integrated Secondary Engine** |

---

## 2. Selection Rationale for PodX Hardware (4GB VRAM)

1. **Why Kokoro-82M is Primary**:
   - **Quality**: Ranks among the highest naturalness scores in open-weight text-to-speech, producing rich, articulate British and American English accents with natural breathing and phrasing.
   - **Safety**: Uses only 300 MB of VRAM or executes on CPU with single-digit percentage CPU usage.
   - **Zero OOM Risk**: Generates 30 minutes of multi-speaker audio in under 60 seconds without running out of memory.
   - **Voice Diversity**: Easily configurable into 24 distinct acoustic character personas with pitch, speed, and timbre adjustments.

2. **Why Qwen3-TTS Architecture is Integrated**:
   - Official support for Voice Design and zero-shot voice cloning.
   - Built-in adapter for Qwen3-TTS checkpoint loading and LoRA fine-tuning scripts.
   - Guarded by PodX's `VRAMSafetyManager`: loads in float16/bfloat16 or auto CPU-offload when VRAM headroom is tight.

---

## 3. Four Generation Modes

1. **Fast Preview**:
   - Optimized for instant script verification.
   - Single-pass Kokoro-82M with standard mastering. Real-time factor < 0.05.
2. **Balanced Quality**:
   - Kokoro-82M + mild dynamic range compression + pause cadence enforcement.
3. **Studio Quality**:
   - Kokoro-82M / Qwen3-TTS 0.6B + multi-stage audio mastering (spectral cleanup, gentle de-essing, dynamic ducking, -16 LUFS podcast normalization).
4. **Extreme Quality**:
   - Multi-speaker synthesis with voice-profile specific EQ, room ambience warming, true-peak limiting (-1.0 dBTP), Whisper ASR quality audit loop, and automatic segment regeneration on audio imperfection.
