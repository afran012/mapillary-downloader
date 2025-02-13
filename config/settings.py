from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    API_KEY: str
    BASE_URL: str = "https://graph.mapillary.com"
    REQUESTS_PER_MINUTE: int = 10000
    DOWNLOAD_PATH: Path = Path("data/downloads")
    LOG_PATH: Path = Path("data/logs")
    BATCH_SIZE: int = 2000
    RETRY_ATTEMPTS: int = 3
    RETRY_DELAY: int = 5

    class Config:
        env_file = ".env"

settings = Settings()