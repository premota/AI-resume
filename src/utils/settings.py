from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM
    model_name: str = "openai:gpt-4o"
    matcher_model_name: str = "anthropic:claude-haiku-4-5-20251001"
    matcher_temperature: float = 0

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/app.db"

    # Auth
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24

    # Redis
    redis_url: str = "redis://localhost:6379"

    # App
    environment: str = "development"
    cors_origins: list[str] = ["http://localhost:3000"]
    sentry_dsn: str = ""


settings = Settings()
