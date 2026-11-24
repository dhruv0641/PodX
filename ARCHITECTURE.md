# PodX System Architecture Specification

---

## 1. High-Level Architecture

PodX is an autonomous, production-grade local AI podcast studio. The architecture decouples front-end user experience, asynchronous job orchestration, modular speech synthesis, and professional digital signal processing.

```
+-----------------------------------------------------------------------------------+
|                            PODX STUDIO FRONTEND (Vite / React / TS)               |
|   - ChatGPT-Style Interface       - Multi-Track Timeline & WaveSurfer             |
|   - 24-Voice Interactive Library  - Fine-Tuning Lab & Dataset Manager             |
|   - Model Manager & Hardware HUD  - Episode History & Audio Export                |
+------------------------------------------+----------------------------------------+
                                           | HTTP REST / Server-Sent Events (SSE)
                                           v
+-----------------------------------------------------------------------------------+
|                               FASTAPI ASYNC BACKEND                               |
|   - API Routers (/chat, /podcasts, /voices, /models, /finetune, /system)          |
|   - Background Task Workers & Resumable Job Queue                                 |
|   - SQLite WAL Persistent Database (SQLAlchemy 2.0 ORM)                          |
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
|  | Kokoro-82M Provider       |  | Qwen3-TTS Provider      |  | Secondary TTS    | |
|  | (Primary Studio / Fast)   |  | (Base/Custom/Quantized) |  | (MOSS / Fallback)| |
|  +---------------------------+  +-------------------------+  +------------------+ |
|  - VRAM Safety Guard: Dynamic offload to CPU if memory headroom < 600 MB          |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                        PROFESSIONAL AUDIO MASTERING CHAIN                         |
|   1. 80Hz High-Pass Filter (Rumble Removal)                                      |
|   2. De-Essing (Sibilance Control 5.5 - 7.5 kHz)                                 |
|   3. Dynamic Compression (2.5:1 ratio, gentle leveling)                          |
|   4. Broadcast Loudness Normalization (-16.0 LUFS Integrated Stereo)              |
|   5. True-Peak Limiter (-1.0 dBTP ceiling)                                        |
|   6. Background Music Ducking & Transition Cross-fades                            |
|   7. Multi-Format Exporter (WAV, MP3 320kbps, FLAC, SRT, VTT, JSON Transcript)    |
+-----------------------------------------------------------------------------------+
```

---

## 2. Key Architecture Pillars

### A. Modular TTS Provider Engine
All speech synthesis models conform to a unified abstract interface: `BaseTTSProvider`.
- `synthesize(text, voice_profile, speed, pitch, emotion) -> AudioSegment`
- `unload() -> None`
- `get_memory_footprint() -> Dict[str, float]`

This ensures new models can be added without modifying backend endpoints or agent logic.

### B. SQLite WAL Persistence
- SQLite in Write-Ahead Logging (`PRAGMA journal_mode=WAL;`) provides ACID guarantees with concurrent readers and non-blocking background writer threads.
- Checkpoints ensure that any segment rendered to disk is instantly persisted; interrupted jobs resume seamlessly from the next unrendered segment.

### C. Audio Mastering Standards
Conforms to EBU R128 and ITU-R BS.1770-4 loudness recommendations:
- Stereo podcasts: **-16.0 LUFS integrated**
- Mono podcasts: **-19.0 LUFS integrated**
- True Peak Ceiling: **-1.0 dBTP**
- Loudness range (LRA): Target 6 to 9 LU for natural spoken dialogue.
