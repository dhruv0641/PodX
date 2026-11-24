"""
PodX Kokoro-82M Model Provider
High-performance, studio-grade speech synthesis via Kokoro ONNX.
Produces 24 kHz broadcast-ready audio with low memory footprint (~300 MB).
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import numpy as np
import scipy.signal
from model_providers.base import BaseTTSProvider

class KokoroTTSProvider(BaseTTSProvider):
    provider_name: str = "kokoro"
    sample_rate: int = 24000

    def __init__(self, model_dir: Optional[str] = None):
        if model_dir is None:
            model_dir = os.path.join(os.getcwd(), "models", "kokoro")
        self.model_dir = Path(model_dir)
        self.onnx_path = self.model_dir / "kokoro-v0_19.onnx"
        self.voices_bin = self.model_dir / "voices-v1.0.bin"
        self.voices_path = self.voices_bin if self.voices_bin.exists() else (self.model_dir / "voices.json")
        self._kokoro_instance = None
        self.is_loaded = False

    def load(self) -> bool:
        if self.is_loaded and self._kokoro_instance is not None:
            return True
        try:
            import kokoro_onnx
            if not self.onnx_path.exists() or not self.voices_path.exists():
                return False
            
            self._kokoro_instance = kokoro_onnx.Kokoro(
                model_path=str(self.onnx_path),
                voices_path=str(self.voices_path)
            )
            self.is_loaded = True
            return True
        except Exception as e:
            print(f"[KokoroTTSProvider] Load failure: {e}")
            self.is_loaded = False
            return False

    def unload(self) -> None:
        self._kokoro_instance = None
        self.is_loaded = False

    def synthesize(
        self,
        text: str,
        voice_id: str = "am_adam",
        speed: float = 1.0,
        pitch: float = 0.0,
        emotion: str = "neutral"
    ) -> Tuple[np.ndarray, int]:
        if not self.is_loaded:
            success = self.load()
            if not success:
                raise RuntimeError("KokoroTTSProvider failed to load ONNX model.")

        # Default fallback voice if unknown
        valid_voices = [
            "af_bella", "af_sarah", "af_nicole", "af_sky", "af_alloy", "af_heart", "af_jessica", "af_kore",
            "am_adam", "am_eric", "am_michael", "am_fenrir", "am_liam", "am_onyx", "am_puck",
            "bf_emma", "bf_isabella", "bf_alice", "bm_george", "bm_lewis"
        ]
        chosen_voice = voice_id if voice_id in valid_voices else "am_adam"

        # Generate audio using Kokoro
        samples, sr = self._kokoro_instance.create(
            text=text,
            voice=chosen_voice,
            speed=speed,
            lang="en-us"
        )
        audio = np.array(samples, dtype=np.float32)

        # Apply subtle pitch modification if needed
        if abs(pitch) > 0.1:
            audio = self._shift_pitch(audio, pitch, sr)

        return audio, sr

    def _shift_pitch(self, audio: np.ndarray, semitones: float, sr: int) -> np.ndarray:
        factor = 2.0 ** (semitones / 12.0)
        indices = np.round(np.arange(0, len(audio), factor))
        indices = indices[indices < len(audio)].astype(int)
        return audio[indices]

    def get_memory_footprint_mb(self) -> Dict[str, float]:
        return {
            "vram_mb": 250.0 if self.is_loaded else 0.0,
            "ram_mb": 350.0 if self.is_loaded else 0.0
        }
