# PodX Architecture Decision Records (ADRs)

---

## ADR-001: Selection of Primary TTS Engine (Kokoro-82M)

### Context
The detected system has an NVIDIA RTX 3050 Laptop GPU with 4,096 MB VRAM and 15.69 GB system RAM. Heavy multi-billion parameter models (e.g. Qwen3-TTS 1.7B, MOSS-TTS 1.2B) require 3.5GB–8GB VRAM in FP16, presenting extreme CUDA OOM failure risks when rendering long-form 20-30 minute podcasts with concurrent OS graphics operations.

### Decision
Select **Kokoro-82M** as the default primary generation engine and preview provider, while implementing a modular provider architecture with **Qwen3-TTS** and **MOSS-TTS** adapters.

### Rationale
- Kokoro-82M delivers studio-grade English acoustic quality with natural prosody and pronunciation.
- Its VRAM footprint is only ~300 MB, operating at 30x–50x real-time speed.
- It can synthesize a 30-minute podcast in under 60 seconds with zero risk of OOM.
- Qwen3-TTS 0.6B and 1.7B are supported via dynamic VRAM management with automatic CPU offload.

---

## ADR-002: SQLite WAL Mode for Persistent Storage

### Context
PodX requires robust local data persistence across restarts, including chat history, generation jobs, audio segments, voice profiles, and fine-tuning metadata. The application must operate offline with zero external database dependencies (e.g., PostgreSQL or Redis).

### Decision
Use **SQLite with Write-Ahead Logging (WAL)** mode enabled (`PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;`).

### Rationale
- Embedded, zero-configuration, cross-platform.
- WAL mode allows concurrent readers while background workers write audio segment records.
- Checkpoints survive abrupt process termination without database corruption.

---

## ADR-003: Strict Script Interpretation vs. Natural Mode

### Context
Users provide precise scripts with stage directions (e.g. `[calm, thoughtful]`, `[pause: 1.5s]`). Naive TTS engines speak these bracketed directives aloud, ruining the podcast.

### Decision
Implement **Strict Script Mode** as default:
1. Regex-based & token-based direction stripping removes all bracketed tags from the speech synthesis stream.
2. Spoken dialogue is preserved verbatim (no words added or deleted).
3. Stage directions are converted into acoustic parameters (emotion, speed, pause duration).
4. An optional **Natural Conversation Mode** is available for LLM-assisted conversational expansion when requested.

---

## ADR-004: Broadcast Audio Mastering Chain

### Context
Raw TTS output often has inconsistent loudness across speakers, harsh high frequencies (sibilance), and low-frequency DC rumble.

### Decision
Incorporate a complete digital signal processing (DSP) mastering chain:
- High-pass 80 Hz filter.
- Dynamic EQ and de-essing (5.5 kHz - 7.5 kHz).
- Gentle dynamic range compression (2.5:1 ratio).
- ITU-R BS.1770-4 loudness normalization to **-16.0 LUFS integrated** with **-1.0 dBTP true-peak ceiling**.
