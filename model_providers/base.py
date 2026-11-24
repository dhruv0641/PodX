"""
PodX Model Providers - Base Interface
Unified abstract interface for all local speech synthesis models.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Optional
import numpy as np

class BaseTTSProvider(ABC):
    """
    Abstract interface for TTS engines integrated into PodX.
    """
    provider_name: str = "base"
    sample_rate: int = 24000
    is_loaded: bool = False

    @abstractmethod
    def load(self) -> bool:
        """Loads weights into memory or initializes runtime session."""
        pass

    @abstractmethod
    def unload(self) -> None:
        """Unloads weights from VRAM/RAM to prevent memory bloat."""
        pass

    @abstractmethod
    def synthesize(
        self,
        text: str,
        voice_id: str,
        speed: float = 1.0,
        pitch: float = 0.0,
        emotion: str = "neutral"
    ) -> Tuple[np.ndarray, int]:
        """
        Synthesizes text into raw float32 PCM audio data.
        Returns (audio_array, sample_rate).
        """
        pass

    @abstractmethod
    def get_memory_footprint_mb(self) -> Dict[str, float]:
        """Returns current RAM and VRAM usage of the provider."""
        pass
