"""
PodX Hardware Discovery & Resource Profiling Module
Autonomously detects system capabilities and generates hardware profiles.
"""
import os
import sys
import json
import platform
import shutil
import subprocess

def get_gpu_info():
    gpu_info = {
        "available": False,
        "name": "None",
        "vram_total_mb": 0,
        "vram_free_mb": 0,
        "driver_version": "N/A",
        "cuda_version": "N/A",
        "backend": "CPU"
    }
    try:
        smi_out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.free,driver_version", "--format=csv,noheader,nounits"],
            encoding="utf-8", stderr=subprocess.DEVNULL
        ).strip()
        if smi_out:
            lines = smi_out.splitlines()
            if lines:
                parts = [p.strip() for p in lines[0].split(",")]
                gpu_info["available"] = True
                gpu_info["name"] = parts[0]
                gpu_info["vram_total_mb"] = float(parts[1])
                gpu_info["vram_free_mb"] = float(parts[2])
                gpu_info["driver_version"] = parts[3]
                gpu_info["backend"] = "CUDA"
                
                # Check cuda version
                nv_full = subprocess.check_output(["nvidia-smi"], encoding="utf-8", stderr=subprocess.DEVNULL)
                for line in nv_full.splitlines():
                    if "CUDA Version" in line:
                        for token in line.split():
                            if token.replace(".", "").isdigit():
                                gpu_info["cuda_version"] = token
                                break
    except Exception:
        pass
    return gpu_info

def get_system_memory():
    total_gb = 16.0
    free_gb = 8.0
    try:
        # On Windows, use wmic or powershell for exact memory
        cmd = ["powershell", "-NoProfile", "-Command", 
               "$os = Get-CimInstance Win32_OperatingSystem; Write-Output \"$($os.TotalVisibleMemorySize),$($os.FreePhysicalMemory)\""]
        out = subprocess.check_output(cmd, encoding="utf-8").strip()
        parts = out.split(",")
        total_kb = float(parts[0])
        free_kb = float(parts[1])
        total_gb = round(total_kb / (1024 * 1024), 2)
        free_gb = round(free_kb / (1024 * 1024), 2)
    except Exception:
        pass
    return total_gb, free_gb

def get_cpu_info():
    name = platform.processor()
    cores_phys = 8
    cores_log = 16
    try:
        cmd = ["powershell", "-NoProfile", "-Command",
               "$cpu = Get-CimInstance Win32_Processor; Write-Output \"$($cpu.Name),$($cpu.NumberOfCores),$($cpu.NumberOfLogicalProcessors)\""]
        out = subprocess.check_output(cmd, encoding="utf-8").strip()
        parts = [p.strip() for p in out.split(",")]
        name = parts[0]
        cores_phys = int(parts[1])
        cores_log = int(parts[2])
    except Exception:
        pass
    return {
        "model": name,
        "physical_cores": cores_phys,
        "logical_cores": cores_log,
        "architecture": platform.machine()
    }

def detect_hardware():
    gpu = get_gpu_info()
    ram_total_gb, ram_free_gb = get_system_memory()
    cpu = get_cpu_info()
    d_disk = shutil.disk_usage("D:\\" if os.path.exists("D:\\") else os.getcwd())
    c_disk = shutil.disk_usage("C:\\" if os.path.exists("C:\\") else os.getcwd())

    # Strategy assessment
    recommended_model = "Kokoro-82M"
    recommended_precision = "fp32" if not gpu["available"] else ("fp16" if gpu["vram_total_mb"] >= 4000 else "fp32")
    max_chunk_chars = 400
    safe_concurrent_speakers = 1
    
    # 4GB VRAM rule: Kokoro-82M is ultra-safe and top quality.
    # Qwen3-TTS 0.6B can fit with offload. Qwen3-TTS 1.7B can fit in quantized/CPU offload mode.
    profile = {
        "timestamp": "2026-11-24T19:25:00Z",
        "system": {
            "os": platform.platform(),
            "os_name": platform.system(),
            "os_version": platform.version(),
            "python_version": platform.python_version()
        },
        "cpu": cpu,
        "ram": {
            "total_gb": ram_total_gb,
            "free_gb": ram_free_gb,
            "sufficient_for_local_tts": ram_total_gb >= 8.0
        },
        "gpu": gpu,
        "storage": {
            "current_drive_free_gb": round(d_disk.free / (1024**3), 2),
            "c_drive_free_gb": round(c_disk.free / (1024**3), 2)
        },
        "capabilities": {
            "cuda_accelerated": gpu["available"],
            "recommended_primary_tts": "kokoro",
            "recommended_advanced_tts": "qwen3-tts-0.6b",
            "fast_preview_provider": "kokoro",
            "recommended_precision": recommended_precision,
            "max_safe_vram_usage_mb": min(3500, int(gpu["vram_total_mb"] * 0.85)) if gpu["available"] else 0,
            "batch_chunk_size": max_chunk_chars,
            "can_train_lora": (gpu["available"] and gpu["vram_total_mb"] >= 4000) or ram_total_gb >= 16.0,
            "safe_concurrent_models": 1
        }
    }
    return profile

if __name__ == "__main__":
    prof = detect_hardware()
    os.makedirs("configs", exist_ok=True)
    with open("configs/hardware_profile.json", "w", encoding="utf-8") as f:
        json.dump(prof, f, indent=2)
    print("Hardware profile generated successfully:")
    print(json.dumps(prof, indent=2))
