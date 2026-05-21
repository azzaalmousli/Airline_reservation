# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Field declarations are required for pydantic-settings to load from .env
    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASSWORD: str = "root"
    DB_NAME: str = "airline_reservation"
    DB_PORT: int = 3306

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+mysqlconnector://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
