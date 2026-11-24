# PodX Changelog

All notable changes and milestones in **PodX — Elite Knowledge AI Podcast Studio** are recorded here.

---

## [1.0.0] - 2026-11-24

### Added
- **Core Architecture**:
  - Modular `BaseTTSProvider` supporting Kokoro-82M, Neural Multi-Accent fallback, and Qwen3-TTS adapters.
  - Native SQLite WAL persistence engine (`db_manager.py`) with thread-safe multi-reader concurrency.
  - Complete digital signal processing mastering chain: 80 Hz high-pass filter, dynamic de-essing, dynamic range compression, ITU-R BS.1770-4 loudness normalization (-16.0 LUFS), and true-peak brickwall limiting (-1.0 dBTP).
- **Voice Library**:
  - 24 unique voice personas (12 Male: M01–M12, 12 Female: F01–F12).
  - Pre-rendered 14–19 second acoustic preview samples for all 24 voices in `storage/previews/`.
  - Natural-language AI Voice Designer for creating custom personas with pitch and speed calibration.
- **Script Intelligence**:
  - `ScriptParser` isolating spoken dialogue from stage directions `[calm, thoughtful]`.
  - Ingestion of explicit pause markers `[pause: 1.5 seconds]`.
  - Sentence-level chunking for long-form episode stability.
- **Frontend Studio**:
  - Production React 18 + TypeScript + Vite + Tailwind CSS dark-charcoal UI.
  - Interactive multi-track timeline with WaveSurfer.js waveform visualizer.
  - 10 dedicated views: Dashboard, New Chat, Podcast Studio, Voice Library, AI Voice Designer, Fine-tuning Lab, Model Manager, Podcast History, Agent Monitor, and System Settings.
  - Single-page application served directly from FastAPI at root `/`.
- **Showcase Master Episode**:
  - Official demonstration podcast: *"The Psychology of Elite Decision Making: Critical Thinking, Mental Models, and Artificial Intelligence"*.
  - Full exports generated: WAV (24-bit), MP3 (320 kbps), SRT, VTT, JSON transcript, and benchmark report.
- **Testing & Tooling**:
  - 12 comprehensive unit and integration tests with 100% pass rate.
  - PowerShell (`scripts/run_podx.ps1`) and Bash (`scripts/run_podx.sh`) single-command launchers.
  - GitHub Actions CI/CD workflow (`.github/workflows/ci.yml`).
