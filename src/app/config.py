from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Content Marketing Assistant"
    environment: str = "development"
    default_channel: str = "linkedin"
    min_draft_length: int = 80
    openai_model: str = "gpt-4.1-mini"
    serp_api_key: str = ""
    openai_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="CONTENTBLITZ_",
        extra="ignore",
    )
