from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.health import router as health_router
from app.api.v1.tickets import router as tickets_router
from app.models.ticket import Ticket
from app.models.user import User
from app.db.session import init_db, Session, engine
from app.services.user_service import UserService
from app.api.v1.users import router as users_router

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

    @app.on_event("startup")
    def on_startup():
        init_db()

        if settings.ENVIRONMENT == "dev":
            with Session(engine) as db:
                user_service = UserService(db)
                existing = user_service.get_user(settings.DEV_ADMIN_USER)
                if not existing:
                    user_service.register_user(
                        username=settings.DEV_ADMIN_USER,
                        email=settings.DEV_ADMIN_EMAIL,
                        password=settings.DEV_ADMIN_PASS
                    )
                    print(f"Dev admin user created → {settings.DEV_ADMIN_USER}/{settings.DEV_ADMIN_PASS}")
                else:
                    print("Dev admin user already exists.")

    app.include_router(health_router, prefix="/api/v1")
    app.include_router(tickets_router, prefix="/api/v1")
    app.include_router(users_router, prefix="/api/v1")
    return app

app = create_app()
