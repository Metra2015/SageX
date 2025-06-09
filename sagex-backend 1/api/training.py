# api/training.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.training import TrainingStart, TrainingEnd, TrainingStatus
from services.training_service import start_training, end_training, get_training_status
from core.database import get_db

router = APIRouter()


@router.post("/start", response_model=TrainingStatus)
def begin_training(data: TrainingStart, db: Session = Depends(get_db)):
    user_id = 1  # Simulated
    started = start_training(db, user_id, data)
    if not started:
        raise HTTPException(status_code=400, detail="You already have an active session.")
    return started


@router.post("/end", response_model=TrainingStatus)
def finish_training(data: TrainingEnd, db: Session = Depends(get_db)):
    user_id = 1  # Simulated
    result = end_training(db, user_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="No active training session found.")
    return result


@router.get("/", response_model=list[TrainingStatus])
def view_all_sessions(db: Session = Depends(get_db)):
    user_id = 1  # Simulated
    return get_training_status(db, user_id)
