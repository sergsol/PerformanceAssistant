"""Application settings, loaded from environment / .env.

The DB URL is swappable: SQLite locally + in tests, Postgres in production
(Render). Because we use SQLModel/SQLAlchemy, only this string changes.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- Core ---
    app_name: str = "Performance Assistant"
    secret_key: str = "dev-only-change-me"  # signs JWTs + sessions; MUST be overridden in prod
    debug: bool = True

    # --- Auth lifetimes ---
    access_token_ttl_minutes: int = 15        # short-lived access token (JWT)
    refresh_token_ttl_days: int = 30          # longer-lived refresh token (server-side, revocable)

    # --- Database ---
    # Local/dev/test default is SQLite. In production set DATABASE_URL to the
    # Render Postgres connection string (postgresql+psycopg://...).
    database_url: str = "sqlite:///./perfreviewbot.db"

    # --- LLM ---
    llm_provider: str = "gemini"          # "gemini" | "groq" | "stub"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.6-flash"
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    # Assessment reproducibility knob for calibration tests
    llm_temperature: float = 0.2


@lru_cache
def get_settings() -> Settings:
    return Settings()
