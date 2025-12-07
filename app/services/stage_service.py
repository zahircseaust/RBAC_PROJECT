from sqlalchemy.orm import Session
from app.repositories.stage_repository import stage_repo
from app.schemas.stage import StageCreate, StageUpdate
from app.exceptions import NotFoundException


class StageService:

    def list(self, db: Session, page: int = 1, page_size: int = 10, search: str = None):
        return stage_repo.get_all(db, page, page_size, search)

    def get(self, db: Session, stage_id: int):
        stage = stage_repo.get_by_id(db, stage_id)
        if not stage:
            raise NotFoundException(resource="Stage", resource_id=stage_id)
        return stage

    def create(self, db: Session, data: StageCreate):
        return stage_repo.create(db, data)

    def update(self, db: Session, stage_id: int, data: StageUpdate):
        stage = stage_repo.get_by_id(db, stage_id)
        if not stage:
            raise NotFoundException(resource="Stage", resource_id=stage_id)
        return stage_repo.update(db, stage, data)

    def delete(self, db: Session, stage_id: int):
        stage = stage_repo.get_by_id(db, stage_id)
        if not stage:
            raise NotFoundException(resource="Stage", resource_id=stage_id)
        return stage_repo.delete(db, stage_id)


stage_service = StageService()
