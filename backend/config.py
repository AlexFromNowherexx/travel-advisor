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
    azure_openai_api_key: str | None = None
    azure_openai_endpoint: str | None = None
    azure_openai_deployment: str | None = None
    search_api_key: str | None = None
    source_mode: str = "strict"
    api_base_url: str = "http://localhost:8000"
    max_sources_per_query: int = 5
    enable_web_search: bool = False
    curated_source_dir: str = "./data/sources"
    demo_short_mode: bool = False
    app_version: str = "0.3.0"
    service_name: str = "bac-bling-agent"
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
