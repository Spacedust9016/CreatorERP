from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    APP_NAME: str = "CreatorERP"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./data/creator_erp.db"

    AI_PROVIDER: str = "local"
    AI_API_KEY: Optional[str] = None
    AI_API_BASE: Optional[str] = None
    AI_MODEL: str = "llama2"

    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    SIMULATED_DATA: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
Path("data").mkdir(exist_ok=True)
