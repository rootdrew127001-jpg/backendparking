from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.health import router as health_router
from app.db.session import init_db
from app.models.ticket import Ticket   
from app.api.v1.tickets_test import router as tickets_test_router
from app.api.v1.tickets import router as tickets_router

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

    @app.on_event("startup")
    def on_startup():
        init_db()      

    app.include_router(health_router, prefix="/api/v1")
    return app


app = create_app()
app.include_router(tickets_test_router, prefix="/api/v1")
app.include_router(tickets_router, prefix="/api/v1")
