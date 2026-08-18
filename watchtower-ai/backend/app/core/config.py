from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "WatchTower AI API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "change-me-to-a-strong-secret"  # replace in prod + use secrets manager
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    S3_ENDPOINT: str = "http://minio:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET: str = "models"
    DATABASE_URL: str = "postgresql+psycopg2://watchtower:watchpass@db:5432/watchtower"

class Config:
        env_file = ".env"

settings = Settings()