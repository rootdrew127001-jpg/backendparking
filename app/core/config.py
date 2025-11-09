from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = Field(default="Campus Parking API")
    DEBUG: bool = Field(default=True)
    DATABASE_URL: str = Field(default="sqlite:///./parking.db", description="DB connection URL")

    class Config:
        env_file = ".env"

settings = Settings()
