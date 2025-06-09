from fastapi import APIRouter
from core.database import SessionLocal

router = APIRouter()

@router.get("/db-check", summary="Check database connectivity")
def check_db():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {"status": "connected"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
