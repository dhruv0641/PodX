# PodX Autonomous Software Engineering Team Specification

This document details the roles, responsibilities, completion criteria, and runtime interaction patterns of the autonomous engineering organization delivering **PodX — Elite Knowledge AI Podcast Studio**.

---

## 1. Development Organization Roster

### 1. Principal Orchestration Agent
- **Responsibilities**: Overall project delivery, task dependency tracking, milestone gate enforcement, autonomous decision recording, cross-team coordination.
- **Completion Criteria**: All 13 project phases executed, verified against acceptance criteria, Git synchronized.

### 2. Technical Research Agent
- **Responsibilities**: Deep research into open-weight TTS architectures (Kokoro, Qwen3-TTS, MOSS-TTS, Chatterbox), licensing audits, hardware viability.
- **Deliverables**: Model evaluation metrics, dependency version pinning, licensing compliance matrix.

### 3. System Architect Agent
- **Responsibilities**: Modular system design, decoupling audio engine from API and frontend, persistent SQLite WAL schema, stateful LangGraph workflow.
- **Deliverables**: `ARCHITECTURE.md`, modular provider interface, data flow schemas.

### 4. Backend Engineering Agent
- **Responsibilities**: FastAPI asynchronous REST API, SSE streaming, SQLite database models, Alembic migrations, background job queue.
- **Deliverables**: `backend/` core application, endpoints for chat, generation, voices, jobs, and exports.

### 5. Frontend Engineering Agent
- **Responsibilities**: React, TypeScript, Vite, Tailwind CSS, TanStack Query, Zustand, WaveSurfer.js waveform visualizer.
- **Deliverables**: Production web app with 10 dedicated views, audio controls, live progress streaming.

### 6. UI/UX Design Agent
- **Responsibilities**: Modern dark-charcoal theme, intuitive chat-to-studio transitions, accessible controls, responsive layout.
- **Deliverables**: Polished studio aesthetics, clear visual indicators, responsive timeline.

### 7. Machine Learning Agent
- **Responsibilities**: TTS provider integrations (Kokoro, Qwen3-TTS adapter, MOSS-TTS stub/provider), model weight management, checkpoint caching.
- **Deliverables**: `model_providers/` modular engine, device-aware model loading.

### 8. Fine-Tuning Agent
- **Responsibilities**: Audio-text dataset ingestion, silence trimming, SNR filtering, LoRA/PEFT training pipeline, validation checkpoints.
- **Deliverables**: `finetuning/` automated training and dataset manager.

### 9. Audio Engineering Agent
- **Responsibilities**: Signal processing chain, LUFS loudness normalization (-16 LUFS stereo), true peak limiting (-1 dBTP), multi-band EQ, de-essing, ducking.
- **Deliverables**: `audio_engine/` mastering and stitching pipeline.

### 10. Performance Engineering Agent
- **Responsibilities**: Memory safety constraints (4GB VRAM guard), chunk streaming, segment disk caching, latency profiling.
- **Deliverables**: Memory guard rails, zero-OOM execution guarantee.

### 11. Security Engineering Agent
- **Responsibilities**: Localhost binding, path traversal prevention, file upload validation, secret scanning, offline operation enforcement.
- **Deliverables**: Sanitized inputs, clean `.gitignore`, isolated storage.

### 12. Quality Assurance Agent
- **Responsibilities**: Test suites (unit, integration, E2E), Faster-Whisper ASR transcript verification, WER/CER calculation, duration audits.
- **Deliverables**: Automated test runners, `TEST_REPORT.md`.

### 13. DevOps Agent
- **Responsibilities**: Environment setup, dependency management, PowerShell and Bash launchers, GitHub Actions CI/CD workflows, Git automation.
- **Deliverables**: `scripts/run_podx.ps1`, `scripts/run_podx.sh`, `.github/workflows/ci.yml`.

### 14. Documentation Agent
- **Responsibilities**: Comprehensive user guides, API references, architecture diagrams, training manuals.
- **Deliverables**: `README.md`, `USER_GUIDE.md`, `TRAINING_GUIDE.md`, `LICENSES.md`.

---

## 2. Runtime Production Agents (Stateful LangGraph Workflow)

During podcast generation, 12 specialized runtime agents execute state transitions:
1. **Master Orchestrator**: Coordinates generation lifecycle, monitors SSE progress, triggers recovery.
2. **Script Intelligence**: Parses markdown/json/tags, strips stage directions `[...]`, extracts speakers.
3. **Podcast Director**: Controls conversational cadence, silence intervals (300-800ms), and scene transitions.
4. **Voice Casting**: Resolves speaker IDs to 24 curated voice profiles, validates model compatibility.
5. **Emotion & Prosody**: Adjusts pitch, rate, and timbre according to script emotion tags.
6. **Pronunciation**: Normalizes acronyms, technical terms, and dates via phonetic dictionary.
7. **Speech Generation**: Calls active TTS provider (Kokoro-82M / Qwen3-TTS) to synthesize raw segment audio.
8. **Continuity**: Enforces voice identity consistency and prevents acoustic drift across turns.
9. **Audio Engineering**: Stitches segments, applies mastering chain (-16 LUFS, true peak limiting, ducking).
10. **Audio QA**: Runs local ASR transcription, computes WER, checks for clipping and hallucinations.
11. **Recovery**: Re-synthesizes defective segments with adjusted seed/temperature (up to 2 retries).
12. **Memory**: Commits episode metadata, audio assets, transcripts, and timeline to SQLite WAL.
