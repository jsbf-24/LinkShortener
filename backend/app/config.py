import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    dynamodb_table: str = os.getenv("DYNAMODB_TABLE", "urls-table")

    class Config:
        env_file = ".env"

settings = Settings()