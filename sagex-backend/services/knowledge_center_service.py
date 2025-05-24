# services/knowledge_center_service.py

from sqlalchemy.orm import Session
from models.knowledge_snapshot import KnowledgeSnapshot
from schemas.knowledge import SnapshotCreate
from datetime import datetime


def create_snapshot(db: Session, user_id: int, data: SnapshotCreate):
    snapshot = KnowledgeSnapshot(
        user_id=user_id,
        symbol=data.symbol.upper(),
        side=data.side.lower(),
        result=data.result.lower(),
        pnl=data.pnl,
        entry_time=data.entry_time,
        exit_time=data.exit_time,
        is_demo=data.is_demo
    )
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot


def get_user_snapshots(db: Session, user_id: int, is_demo: bool = False):
    return db.query(KnowledgeSnapshot).filter(
        KnowledgeSnapshot.user_id == user_id,
        KnowledgeSnapshot.is_demo == is_demo
    ).order_by(KnowledgeSnapshot.created_at.desc()).all()
