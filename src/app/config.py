from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Content Marketing Assistant"
    ENVIRONMENT: str = "development"
    DEFAULT_PLATFORM: str = "linkedin"
    DEFAULT_TONE: str = "professional"
    MAX_ITERATIONS: int = 2
    MIN_DRAFT_LENGTH: int = 80
    OPENAI_MODEL: str = "gpt-4"
    SERPAPI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",
        extra="ignore",
    )


settings = Settings()
