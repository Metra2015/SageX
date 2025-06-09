from fastapi import APIRouter
from sqlalchemy import text
from core.database import SessionLocal

router = APIRouter()

@router.get("/db-check", summary="Check database connectivity")
def check_db():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "connected"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
