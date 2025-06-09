# services/open_position_service.py

from sqlalchemy.orm import Session
from models.open_position import OpenPosition
from schemas.open_position import OpenPositionCreate
from typing import List


def create_open_position(db: Session, data: OpenPositionCreate) -> OpenPosition:
    position = OpenPosition(**data.dict())
    db.add(position)
    db.commit()
    db.refresh(position)
    return position


def get_user_open_positions(db: Session, user_id: int, is_demo: bool = True) -> List[OpenPosition]:
    return db.query(OpenPosition).filter(
        OpenPosition.user_id == user_id,
        OpenPosition.is_demo == is_demo
    ).all()


def close_position_by_id(db: Session, position_id: int):
    position = db.query(OpenPosition).filter(OpenPosition.id == position_id).first()
    if position:
        db.delete(position)
        db.commit()
    return position
