from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Campus Parking API"
    DEBUG: bool = True
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


    ENVIRONMENT: str = "dev"  
    DEV_ADMIN_USER: str = "admin"
    DEV_ADMIN_PASS: str = "admin"
    DEV_ADMIN_EMAIL: str = "admin@example.com"

    class Config:
        env_file = ".env"

settings = Settings()