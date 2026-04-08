"""Application configuration via pydantic-settings.

Settings are loaded from environment variables (and .env file if present).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "Python App Template"
    app_slug: str = "python-app"
    deployment: str = "dev"
    debug: bool = False

    # Database — SQLite by default, swap DATABASE_URL for Postgres
    database_url: str = "sqlite:///./data/app.db"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Session / security
    secret_key: str = "dev-secret-key-change-in-production"


settings = Settings()
