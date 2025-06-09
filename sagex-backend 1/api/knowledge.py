# api/knowledge.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.knowledge import SnapshotCreate, SnapshotResponse
from services.knowledge_center_service import create_snapshot, get_user_snapshots
from core.database import get_db

router = APIRouter()


@router.post("/", response_model=SnapshotResponse)
def log_snapshot(data: SnapshotCreate, db: Session = Depends(get_db)):
    user_id = 1  # Simulated user
    return create_snapshot(db, user_id, data)


@router.get("/", response_model=list[SnapshotResponse])
def view_snapshots(is_demo: bool = False, db: Session = Depends(get_db)):
    user_id = 1  # Simulated user
    return get_user_snapshots(db, user_id, is_demo)
