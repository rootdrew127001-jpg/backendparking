from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.health import router as health_router

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)
    app.include_router(health_router, prefix="/api/v1")
    return app

app = create_app()
