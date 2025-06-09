# core/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "SageX"
    API_V1_STR: str = "/api"
    DB_URL: str = "sqlite:///./sagex.db"  # Replace with PostgreSQL/MySQL if needed
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
