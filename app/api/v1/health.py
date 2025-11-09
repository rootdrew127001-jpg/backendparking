from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
def health():
    return {
        "status": "ok",
        "service": "campus-parking-api",
        "time": datetime.utcnow().isoformat() + "Z",
        "checks": {"api": True}
    }
