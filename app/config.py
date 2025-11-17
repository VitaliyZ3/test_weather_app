from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    openweather_api_key: str | None = None
    openweather_base_url: str = "https://api.openweathermap.org/data/2.5/weather"
    cache_ttl_seconds: int = 300  # 5 minutes
    data_dir: str = "./data"
    sqlite_path: str = "./weather_logs.db"
    rate_limit_per_minute: int = 30

    class Config:
        env_file = os.getenv("ENV_FILE", ".env")
        env_file_encoding = "utf-8"

settings = Settings()