from sqlalchemy.orm import Session
from app.repositories.stage_repository import stage_repo
from app.schemas.stage import StageCreate, StageUpdate


class StageService:

    def list(self, db: Session):
        return stage_repo.get_all(db)

    def get(self, db: Session, stage_id: int):
        return stage_repo.get_by_id(db, stage_id)

    def create(self, db: Session, data: StageCreate):
        return stage_repo.create(db, data)

    def update(self, db: Session, stage_id: int, data: StageUpdate):
        stage = stage_repo.get_by_id(db, stage_id)
        if not stage:
            return None
        return stage_repo.update(db, stage, data)

    def delete(self, db: Session, stage_id: int):
        return stage_repo.delete(db, stage_id)


stage_service = StageService()
