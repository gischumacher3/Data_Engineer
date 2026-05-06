from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Product Error Intelligence Pipeline"
    app_env: str = Field(default="development", alias="APP_ENV")
    database_url: str = Field(default="sqlite:///./product_error_intelligence.db", alias="DATABASE_URL")
    cors_origins: str = Field(default="http://localhost:5173", alias="CORS_ORIGINS")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
