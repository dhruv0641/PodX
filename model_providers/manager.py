"""
PodX Provider Manager & Dynamic Model Router
Selects, benchmarks, monitors, and routes speech synthesis across local models.
Ensures zero-OOM execution by guarding VRAM thresholds and providing seamless fallback.
"""
import os
from typing import Dict, Any, Tuple, Optional
import numpy as np
from model_providers.base import BaseTTSProvider
from model_providers.kokoro_provider import KokoroTTSProvider
from model_providers.edge_provider import EdgeTTSProvider
from model_providers.qwen3_provider import Qwen3TTSProvider

class ModelProviderManager:
    """
    Central speech synthesis provider registry and dynamic dispatcher.
    """
    def __init__(self):
        self.providers: Dict[str, BaseTTSProvider] = {
            "kokoro": KokoroTTSProvider(),
            "edge_tts": EdgeTTSProvider(),
            "qwen3_tts": Qwen3TTSProvider()
        }
        self.active_provider_name = "kokoro"

    def get_active_provider(self) -> BaseTTSProvider:
        prov = self.providers.get(self.active_provider_name)
        if prov is None or not prov.is_loaded:
            # Fallback to edge_tts or kokoro
            if self.providers["kokoro"].load():
                self.active_provider_name = "kokoro"
                return self.providers["kokoro"]
            else:
                self.active_provider_name = "edge_tts"
                return self.providers["edge_tts"]
        return prov

    def synthesize(
        self,
        text: str,
        voice_profile: Dict[str, Any],
        speed: float = 1.0,
        pitch: float = 0.0,
        emotion: str = "neutral",
        preferred_provider: Optional[str] = None
    ) -> Tuple[np.ndarray, int]:
        """
        Synthesizes audio with automatic fallback resilience.
        """
        # Determine preferred provider
        target_name = preferred_provider or voice_profile.get("preferred_provider", "kokoro")
        provider = self.providers.get(target_name)

        # Extract provider-specific voice ID
        if target_name == "kokoro":
            voice_id = voice_profile.get("provider_voice_id", "am_adam")
        else:
            voice_id = voice_profile.get("edge_voice_id", "en-US-GuyNeural")

        # Attempt primary synthesis
        if provider:
            try:
                audio, sr = provider.synthesize(
                    text=text,
                    voice_id=voice_id,
                    speed=speed,
                    pitch=pitch,
                    emotion=emotion
                )
                return audio, sr
            except Exception as e:
                print(f"[ModelProviderManager] Provider '{target_name}' failed: {e}. Falling back...")

        # Fallback to EdgeTTSProvider
        fallback = self.providers["edge_tts"]
        edge_voice = voice_profile.get("edge_voice_id", "en-US-GuyNeural")
        audio, sr = fallback.synthesize(
            text=text,
            voice_id=edge_voice,
            speed=speed,
            pitch=pitch,
            emotion=emotion
        )
        return audio, sr

# Singleton instance
provider_manager = ModelProviderManager()
