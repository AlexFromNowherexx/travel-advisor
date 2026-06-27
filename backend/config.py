from pathlib import Path

# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)


class Settings(BaseSettings):
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    serpapi_api_key: str | None = None
    serpapi_limit: int = 5
    skill_file_path: str = "skills/travel-consultant/SKILL.md"
    cors_origins: list[str] = ["http://localhost:8501"]
    tts_engine: str = "pyttsx3"
    tts_voice: str | None = None
    tts_rate: int = 180
    tts_volume: float = 1.0

    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore")


settings = Settings()
