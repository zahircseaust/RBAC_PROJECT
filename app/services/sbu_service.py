from sqlalchemy.orm import Session
from app.repositories.sbu_repository import sbu_repo
from app.schemas.sbu import SBUCreate, SBUUpdate

class SBUService:

    def list(self, db: Session):
        return sbu_repo.get_all(db)

    def get(self, db: Session, sbu_id: int):
        return sbu_repo.get_by_id(db, sbu_id)

    def create(self, db: Session, data: SBUCreate):
        return sbu_repo.create(db, data)

    def update(self, db: Session, sbu_id: int, data: SBUUpdate):
        sbu = sbu_repo.get_by_id(db, sbu_id)
        if not sbu:
            return None
        return sbu_repo.update(db, sbu, data)

    def delete(self, db: Session, sbu_id: int):
        return sbu_repo.delete(db, sbu_id)

sbu_service = SBUService()
