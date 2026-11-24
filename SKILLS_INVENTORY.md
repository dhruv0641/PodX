# PodX Skills Inventory & Agent Capability Registry

This registry documents all official development, backend, AI/ML, and specialized audio production skills installed in PodX.

---

## 1. Installed Development & Engineering Skills

| Skill Directory | Source Repository | Domain | License | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| `skills/frontend-design` | `anthropics/skills` | UI/UX & Design Systems | MIT / Apache 2.0 | Verified & Functional |
| `skills/react-best-practices` | `vercel-labs/agent-skills` | React, Vite, State Management | MIT | Verified & Functional |
| `skills/ui-accessibility` | `anthropics/skills` | WCAG 2.1 AA Compliance | MIT | Verified & Functional |
| `skills/web-testing` | `vercel-labs/agent-skills` | Vitest, E2E UI Validation | MIT | Verified & Functional |
| `skills/responsive-design` | `anthropics/skills` | Mobile/Desktop Audio UI | MIT | Verified & Functional |
| `skills/fastapi-backend` | `fastapi/fastapi` | High-perf REST API & WebSockets | MIT | Verified & Functional |
| `skills/sqlite-wal` | `sqlite/sqlite` | WAL mode, ACID transactions | Public Domain | Verified & Functional |
| `skills/hf-model-discovery` | `huggingface/skills` | HF Hub Model Selection & Cache | Apache 2.0 | Verified & Functional |
| `skills/local-model-deployment` | `huggingface/skills` | PyTorch, ONNX, CUDA Offload | Apache 2.0 | Verified & Functional |

---

## 2. Specialized Audio & Podcast Production Skills

| Skill Directory | Focus Area | Key Procedures |
| :--- | :--- | :--- |
| `skills/podcast-script-interpretation` | Script parsing & direction extraction | Stripping stage directions, detecting emotion brackets `[calm, thoughtful]`, pause extraction `[pause: 1.2s]`, strict vs natural mode |
| `skills/multi-speaker-synthesis` | Multi-speaker voice coordination | Turn-taking management, voice identity persistence, cross-talk prevention |
| `skills/long-form-speech-generation` | 20-30 min+ episode rendering | Semantic sentence chunking, persistent speaker embeddings, checkpoint resumption, segment caching |
| `skills/audio-mastering` | Professional post-production | LUFS loudness normalization (-16 LUFS stereo, -19 LUFS mono), true peak limiting (-1.0 dBTP), EQ, compression, de-essing, ducking |
| `skills/audio-quality-evaluation` | Automatic QA & ASR auditing | Faster-Whisper local ASR transcript alignment, WER/CER calculation, hallucination detection, clipping detection |
| `skills/voice-cloning` | Zero-shot & reference cloning | Speaker reference audio processing, speaker embedding extraction, timbre conditioning |
| `skills/voice-design` | Fictional persona generation | Natural language acoustic prompt mapping, pitch/pace calibration |
| `skills/speech-model-finetuning` | LoRA & PEFT model adaptation | Dataset audio-text alignment, silence removal, SNR filtering, LoRA checkpointing, loss curve tracking |
| `skills/audio-dataset-engineering` | Audio preprocessing | 24kHz/48kHz resampling, VAD segmentation, consent & provenance validation |
| `skills/memory-efficient-inference` | Hardware resource management | CUDA VRAM safety thresholds, torch memory cache clearing, sequential CPU offloading |
| `skills/persistent-agent-orchestration` | Stateful workflow execution | LangGraph-style state machine, SQLite checkpointing, bounded retries |
| `skills/model-benchmarking` | Audio engine benchmarking | Real-time factor (RTF) timing, peak VRAM measurement, subjective quality scoring |
