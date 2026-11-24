"""
PodX Edge-TTS Neural Provider
Reliable, multi-accent, zero-VRAM speech synthesis engine.
Provides natural conversational voices across American, British, and Indian accents.
"""
import io
import asyncio
import tempfile
import numpy as np
import soundfile as sf
from typing import Dict, Any, Tuple
from model_providers.base import BaseTTSProvider

class EdgeTTSProvider(BaseTTSProvider):
    provider_name: str = "edge_tts"
    sample_rate: int = 24000
    is_loaded: bool = True

    def load(self) -> bool:
        self.is_loaded = True
        return True

    def unload(self) -> None:
        pass

    def synthesize(
        self,
        text: str,
        voice_id: str = "en-US-GuyNeural",
        speed: float = 1.0,
        pitch: float = 0.0,
        emotion: str = "neutral"
    ) -> Tuple[np.ndarray, int]:
        import edge_tts

        # Rate and pitch formatting: e.g. "+5%", "-2Hz"
        rate_percent = int((speed - 1.0) * 100)
        rate_str = f"{rate_percent:+d}%" if rate_percent != 0 else "+0%"

        pitch_hz = int(pitch * 4)
        pitch_str = f"{pitch_hz:+d}Hz" if pitch_hz != 0 else "+0Hz"

        async def _run_synthesis():
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice_id,
                rate=rate_str,
                pitch=pitch_str
            )
            mp3_bytes = bytearray()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    mp3_bytes.extend(chunk["data"])
            return bytes(mp3_bytes)

        # Execute async generation
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If running inside existing event loop
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    audio_data = pool.submit(asyncio.run, _run_synthesis()).result()
            else:
                audio_data = loop.run_until_complete(_run_synthesis())
        except Exception:
            audio_data = asyncio.run(_run_synthesis())

        # Decode MP3 to float32 numpy array
        bio = io.BytesIO(audio_data)
        data, sr = sf.read(bio, dtype='float32')

        # Ensure mono
        if data.ndim > 1:
            data = np.mean(data, axis=1)

        return data, sr

    def get_memory_footprint_mb(self) -> Dict[str, float]:
        return {"vram_mb": 0.0, "ram_mb": 60.0}
