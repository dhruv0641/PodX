# PodX — Elite Knowledge AI Podcast Studio

<div align="center">

![PodX Banner](https://img.shields.io/badge/PodX-AI%20Podcast%20Studio-8b5cf6?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-10b981?style=for-the-badge)
![Audio Standard](https://img.shields.io/badge/Standard-EBU%20R128%20(-16%20LUFS)-06b6d4?style=for-the-badge)
![Local Operation](https://img.shields.io/badge/Operation-100%25%20Offline%20Local-f59e0b?style=for-the-badge)
![License](https://img.shields.io/badge/License-Apache%202.0%20%2F%20MIT-3b82f6?style=for-the-badge)

**Autonomous local AI podcast generation platform transforming user-provided scripts into broadcast-grade, natural, multi-speaker conversational audio.**

</div>

---

## 🎙️ Executive Summary

**PodX (Elite Knowledge AI Podcast Studio)** is an autonomous, production-quality local audio production platform. Designed from first principles to prioritize audio fidelity, script precision, emotional intelligence, character continuity, and 100% offline privacy, PodX converts raw scripts into fully mastered 20–30+ minute podcast episodes adhering to international broadcast standards (EBU R128 / ITU-R BS.1770-4 at -16.0 LUFS integrated and -1.0 dBTP true-peak ceiling).

Unlike rudimentary text-to-speech wrappers, PodX delivers an end-to-end digital audio workstation (DAW) and agentic production suite:
- **Strict Script Intelligence**: Automatically separates spoken dialogue from bracketed stage directions (e.g. `[calm, thoughtful]`, `(laughter)`) and translates pause directives (`[pause: 1.5s]`) into precise acoustic silences without ever reading stage directions aloud.
- **24 Curated Voice Personas**: 12 Male and 12 Female fictional personas spanning American, British, and Indian English accents, each calibrated for distinct pitch, speed, and timbre.
- **Resumable Multi-Agent Production**: 12 specialized runtime agents coordinate script analysis, casting, directing, synthesis, acoustic continuity, DSP mastering, and automated speech recognition (ASR) quality audits.
- **Broadcast Mastering Chain**: 80 Hz high-pass rumble filter, dynamic de-essing, dynamic range leveling, -16.0 LUFS loudness normalization, and -1.0 dBTP true-peak brickwall limiting.
- **Zero-OOM Hardware Safety**: Dynamic resource management optimized for host hardware (NVIDIA RTX 3050 Laptop GPU 4GB VRAM, 16GB RAM) with instant CPU-offload fallback.
- **Persistent SQLite WAL Persistence**: Resilient Write-Ahead Logging database ensuring zero data loss across restarts, segment caching, and selective sentence-level regeneration.

---

## 🏛️ System Architecture

```
+-----------------------------------------------------------------------------------+
|                            PODX STUDIO FRONTEND (Vite / React / TS)               |
|   - ChatGPT-Style Script Ingestion     - Multi-Track Timeline & WaveSurfer        |
|   - 24-Voice Interactive Library       - Fine-Tuning Lab & Dataset Manager        |
|   - Model Manager & Hardware HUD       - Episode History & Multi-Format Exporter  |
+------------------------------------------+----------------------------------------+
                                           | HTTP REST / Server-Sent Events (SSE)
                                           v
+-----------------------------------------------------------------------------------+
|                               FASTAPI ASYNC BACKEND                               |
|   - Routers (/api/chat, /api/podcasts, /api/voices, /api/models, /api/finetuning) |
|   - Asynchronous Background Workers & Resumable Checkpoint Queue                  |
|   - Native SQLite WAL Persistence Engine (Thread-Safe & Zero-Dependency)          |
+------------------------------------------+----------------------------------------+
                                           |
                   +-----------------------+-----------------------+
                   v                                               v
+------------------------------------+           +----------------------------------+
|     LANGGRAPH AGENT WORKFLOW       |           |        STORAGE SUBSYSTEM         |
|  - Script Intelligence & Stripping |           |  - /storage/audio (Segments)     |
|  - Podcast Director & Pacing       |           |  - /storage/exports (MP3/WAV/etc)|
|  - Voice Casting & Prosody Engine  |           |  - /storage/previews (Voices)    |
|  - Continuity & Segment QA Loop    |           |  - /storage/podx.db (SQLite WAL) |
+------------------+-----------------+           +----------------------------------+
                   |
                   v
+-----------------------------------------------------------------------------------+
|                            MODULAR AUDIO GENERATION ENGINE                        |
|  +---------------------------+  +-------------------------+  +------------------+ |
|  | Kokoro-82M Provider       |  | Neural Multi-Accent     |  | Qwen3-TTS LoRA   | |
|  | (Studio Production / Fast)|  | (Zero-VRAM Fallback)    |  | (Adaptation Engine|
|  +---------------------------+  +-------------------------+  +------------------+ |
|  - VRAM Safety Guard: Dynamic offload to CPU if memory headroom < 600 MB          |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                        PROFESSIONAL AUDIO MASTERING CHAIN                         |
|   1. 80Hz High-Pass Filter (Rumble & DC Offset Removal)                           |
|   2. De-Essing (Sibilance Control 5.5 - 7.5 kHz)                                  |
|   3. Dynamic Compression (2.5:1 ratio, smooth dialogue leveling)                  |
|   4. Broadcast Loudness Normalization (-16.0 LUFS Integrated Stereo)              |
|   5. True-Peak Limiter (-1.0 dBTP ceiling to eliminate inter-sample clipping)     |
|   6. Background Music Ducking & Transition Cross-fades                            |
|   7. Multi-Format Exporter (WAV 24-bit, MP3 320kbps, FLAC, SRT, VTT, JSON)        |
+-----------------------------------------------------------------------------------+
```

---

## 👥 Voice Persona Library (24 Distinct Profiles)

PodX includes 24 unique, original fictional voice personas with pre-rendered acoustic preview samples:

### Male Voices (M01 – M12)
| ID | Name | Accent | Persona Description | Preferred Provider |
| :--- | :--- | :--- | :--- | :--- |
| **M01** | Alexander | American | Deep, sophisticated, authoritative, intellectual and composed. | Kokoro / Neural |
| **M02** | James | British | Warm British accent, articulate, refined and analytical. | Kokoro / Neural |
| **M03** | Ethan | American | Modern American technology podcast host, confident and energetic. | Kokoro / Neural |
| **M04** | Marcus | American | Rich baritone, cinematic, serious and philosophical. | Kokoro / Neural |
| **M05** | Oliver | British | Curious, friendly, intelligent and conversational. | Kokoro / Neural |
| **M06** | Daniel | American | Calm documentary narrator with excellent pronunciation. | Kokoro / Neural |
| **M07** | Adrian | American | Professional business and financial analysis presenter. | Kokoro / Neural |
| **M08** | Victor | American | Powerful, mature, strategic and authoritative executive. | Kokoro / Neural |
| **M09** | Noah | American | Youthful, approachable and naturally expressive. | Kokoro / Neural |
| **M10** | Arjun | Indian English | Clear Indian English, articulate, analytical and professional. | Kokoro / Neural |
| **M11** | Sebastian | British | Refined, thoughtful and suitable for history and psychology. | Kokoro / Neural |
| **M12** | Gabriel | American | Relaxed, reflective and emotionally engaging storyteller. | Kokoro / Neural |

### Female Voices (F01 – F12)
| ID | Name | Accent | Persona Description | Preferred Provider |
| :--- | :--- | :--- | :--- | :--- |
| **F01** | Sophia | American | Intelligent, elegant, confident and articulate. | Kokoro / Neural |
| **F02** | Olivia | British | Warm, refined British conversational voice. | Kokoro / Neural |
| **F03** | Emma | American | Energetic American podcast presenter. | Kokoro / Neural |
| **F04** | Isabella | American | Sophisticated, mature and documentary-oriented. | Kokoro / Neural |
| **F05** | Ava | American | Curious, friendly and naturally expressive. | Kokoro / Neural |
| **F06** | Victoria | British | Authoritative, professional and analytical. | Kokoro / Neural |
| **F07** | Amelia | American | Calm, clear and suitable for educational explanations. | Kokoro / Neural |
| **F08** | Elena | American | Thoughtful, philosophical and emotionally expressive. | Kokoro / Neural |
| **F09** | Maya | Indian English | Professional Indian English with natural articulation. | Kokoro / Neural |
| **F10** | Charlotte | British | Elegant, composed and suitable for elite business discussions. | Kokoro / Neural |
| **F11** | Aurora | American | Cinematic, immersive and excellent for storytelling. | Kokoro / Neural |
| **F12** | Claire | American | Natural, intelligent and suitable for technical conversations. | Kokoro / Neural |

---

## ⚡ Quick Start & Installation

### Prerequisites
- Python 3.11+
- Node.js v18+ and npm
- FFmpeg (available in system PATH)
- NVIDIA GPU with CUDA (optional; runs with full performance on CPU)

### Launching on Windows (PowerShell)
```powershell
.\scripts\run_podx.ps1
```

### Launching on Linux / macOS (Bash)
```bash
chmod +x scripts/run_podx.sh
./scripts/run_podx.sh
```

Once started, open your web browser at:
👉 **`http://127.0.0.1:8001`**

---

## 🔬 Four Generation Modes

1. **Fast Preview**: Instant verification with 50x real-time speed.
2. **Balanced Quality**: Studio synthesis with mild dynamic range leveling.
3. **Studio Quality**: Multi-stage audio mastering (spectral cleanup, de-essing, -16 LUFS podcast normalization).
4. **Extreme Quality**: Full multi-speaker synthesis with voice-profile specific EQ, room ambience warming, true-peak limiting (-1.0 dBTP), and automated QA verification.

---

## 📦 Multi-Format Artifact Exports

For every generated episode, PodX produces:
- `master_podcast.wav`: 24-bit 48kHz uncompressed production master
- `master_podcast.mp3`: 320 kbps broadcast MP3
- `transcript.srt`: SubRip subtitle timing with speaker tags
- `transcript.vtt`: WebVTT subtitles with millisecond alignment
- `transcript.json`: Structured transcript with segment durations and acoustic metadata
- `benchmark_and_qa_report.json`: Detailed loudness, peak dBTP, and QA audit results

---

## 🛡️ Privacy, Security & Ethics

- **100% Local Execution**: All synthesis and mastering execute locally on `127.0.0.1`. No audio data, scripts, or user queries are transmitted to external cloud APIs.
- **Strict Consent Verification**: The fine-tuning lab enforces mandatory provenance declarations and consent verification before registering any voice training dataset.
- **Fictional Personas**: All default voice profiles are original fictional characters, preventing unauthorized impersonation of real public figures.
