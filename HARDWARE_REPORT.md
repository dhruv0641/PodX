# PodX Hardware Discovery & Capability Profile

**Autonomous System Hardware Audit Report**  
*Generated on: 2026-11-24*

---

## 1. System Overview

| Parameter | Detected Value | Verification Method |
| :--- | :--- | :--- |
| **Operating System** | Windows 11 / Windows 10 (Build 10.0.26200-SP0) | Win32_OperatingSystem / Platform |
| **Architecture** | AMD64 (x86_64) | Python `platform.machine()` |
| **Python Environment** | Python 3.11.9 (64-bit) | `.venv\Scripts\python.exe` |
| **Node.js Environment** | Node.js v24.21.0, npm 11.19.0 | CLI execution |
| **FFmpeg Status** | 9.0.2-full_build (Gyan.dev) with libmp3lame, libopus, flac, aac | `ffmpeg -version` |
| **Git Version** | Git 2.55.0.windows.5 | `git --version` |

---

## 2. Processor & Memory

- **CPU Model**: 12th Gen Intel(R) Core(TM) i5-12500H
- **Physical Cores**: 12
- **Logical Threads**: 16
- **Instruction Sets**: AVX2, FMA, SSE4.2, Intel DL Boost
- **Total System RAM**: 15.69 GB (approx. 16 GB physical)
- **Available System RAM**: 1.89 GB - 8.0 GB dynamic
- **Storage Free Space**:
  - `D:\` Drive (Workspace): **231.31 GB Free**
  - `C:\` Drive (System): **261.53 GB Free**

---

## 3. GPU Acceleration & VRAM

- **GPU Device**: NVIDIA GeForce RTX 3050 Laptop GPU
- **Dedicated VRAM**: 4,096 MiB (4.00 GB)
- **Driver Version**: 581.95
- **CUDA Runtime / Driver Capability**: CUDA 13.0 / 12.x compatible
- **DirectX / Vulkan**: Supported

---

## 4. Hardware Sizing & Dynamic Resource Allocation

| Resource Metric | Hardware Boundary | Safe PodX Allocation Limit |
| :--- | :--- | :--- |
| **Max VRAM per Model** | 4,096 MB | **3,480 MB** (leaving 600 MB for OS window manager/display) |
| **Model In-Memory Policy** | Multi-model prohibited | **Single active heavyweight model**, dynamic load/unload |
| **Primary Production Engine** | Kokoro-82M (FP16 / INT8) | ~300 MB VRAM footprint; ultra-fast (20x-50x realtime) |
| **Advanced Research Engine** | Qwen3-TTS 0.6B Base / Custom | Fits within 2.5 GB VRAM in FP16 or CPU offload |
| **Heavy 1.7B+ Models** | Qwen3-TTS 1.7B / MOSS-TTS | Offloaded to CPU or 4-bit quantized to prevent CUDA OOM |
| **Long-form Batch Strategy** | Segment chunking | 200–400 character natural sentence chunks |
| **Audio Mastering** | CPU Multi-threading | 8 worker threads for FFT, LUFS, compression & limiting |

---

## 5. Architectural Recommendations

1. **Dual Engine Runtime**:
   - **Kokoro-82M**: Designated as the primary production engine for Instant Preview, Balanced Quality, and resilient Studio Generation. High-fidelity 24 kHz audio with negligible VRAM requirements and zero OOM failure risk.
   - **Qwen3-TTS / MOSS Engine**: Modular adapter with automatic VRAM fallback. If CUDA allocations exceed 3.5 GB, inference gracefully routes or falls back without crashing the job.
2. **Audio Post-Production**:
   - Utilize native FFmpeg + SoundFile + Librosa + NumPy pipeline for Broadcast Podcast mastering (-16 LUFS stereo, -1 dBTP ceiling, dynamic smoothing).
