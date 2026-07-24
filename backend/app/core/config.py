from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ==========================================================
    # Project
    # ==========================================================

    PROJECT_NAME: str = Field(default="Cluster Doctor API")
    API_VERSION: str = Field(default="v1")
    DEBUG: bool = Field(default=True)

    # ==========================================================
    # Database
    # ==========================================================

    DATABASE_URL: str

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # ==========================================================
    # Redis
    # ==========================================================

    REDIS_HOST: str
    REDIS_PORT: int

    # ==========================================================
    # MQTT
    # ==========================================================

    MQTT_HOST: str
    MQTT_PORT: int

    # ==========================================================
    # Security
    # ==========================================================

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # ==========================================================
    # OpenAI / LLM
    # ==========================================================

    OPENAI_API_KEY: str
    OPENAI_MODEL: str = Field(default="gpt-4.1-mini")
    OPENAI_BASE_URL: str = Field(default="https://openrouter.ai/api/v1")

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()