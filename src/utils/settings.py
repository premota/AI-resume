from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    model_name: str = "openai:gpt-4o" # for cv and jd parsing
    matcher_model_name: str = "anthropic:claude-haiku-4-5-20251001" # for cv and jd comparison
    matcher_temperature: float = 0


# create a global settings
settings = Settings()