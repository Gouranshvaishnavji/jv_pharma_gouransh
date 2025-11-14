# app/core/config.py
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv() 

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):


    APP_NAME: str = os.getenv("APP_NAME", "my-biotech")
    ENV: str = os.getenv("ENV", "dev")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")

    BASE_DIR: Path = BASE_DIR
    UPLOAD_DIR: Path = BASE_DIR / os.getenv("UPLOAD_DIR", "data/uploads")
    VECTOR_DB_PATH: Path = BASE_DIR / os.getenv("VECTOR_DB_PATH", "data/vectorstore")
    LOG_DIR: Path = BASE_DIR / os.getenv("LOG_DIR", "logs")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

for path in [settings.UPLOAD_DIR, settings.VECTOR_DB_PATH, settings.LOG_DIR]:
    os.makedirs(path, exist_ok=True)
