from sqlalchemy.orm import Session
from app.models.sbus import SBU
from app.schemas.sbu import SBUCreate, SBUUpdate

class SBURepository:

    def get_all(self, db: Session):
        return db.query(SBU).all()

    def get_by_id(self, db: Session, sbu_id: int):
        return db.query(SBU).filter(SBU.id == sbu_id).first()

    def create(self, db: Session, obj_in: SBUCreate):
        sbu = SBU(**obj_in.dict())
        db.add(sbu)
        db.commit()
        db.refresh(sbu)
        return sbu

    def update(self, db: Session, db_obj: SBU, obj_in: SBUUpdate):
        data = obj_in.dict(exclude_unset=True)
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, sbu_id: int):
        obj = self.get_by_id(db, sbu_id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

sbu_repo = SBURepository()
