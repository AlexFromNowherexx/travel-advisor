from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import tempfile
from threading import Lock

# pyrefly: ignore [missing-import]
import pyttsx3

from .config import settings

_engine_lock = Lock()


@lru_cache(maxsize=1)
def get_engine():
    engine = pyttsx3.init()
    engine.setProperty("rate", settings.tts_rate)
    engine.setProperty("volume", settings.tts_volume)

    if settings.tts_voice:
        voices = engine.getProperty("voices") or []
        for voice in voices:
            voice_id = str(getattr(voice, "id", ""))
            voice_name = str(getattr(voice, "name", ""))
            if settings.tts_voice in {voice_id, voice_name}:
                engine.setProperty("voice", voice_id)
                break

    return engine


def synthesize_wav_bytes(text: str) -> bytes:
    with _engine_lock:
        engine = get_engine()
        tmp_path = Path(tempfile.mkstemp(suffix=".wav")[1])
        try:
            engine.save_to_file(text, str(tmp_path))
            engine.runAndWait()
            return tmp_path.read_bytes()
        finally:
            try:
                tmp_path.unlink(missing_ok=True)
            except OSError:
                pass
