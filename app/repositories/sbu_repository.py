from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.sbus import SBU
from app.schemas.sbu import SBUCreate, SBUUpdate

class SBURepository:

    def get_all(self, db: Session, page: int = 1, page_size: int = 10, search: str = None):
        query = db.query(SBU).filter(SBU.is_deleted == False)

        # Apply search filter
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    SBU.name.ilike(search_filter),
                    SBU.description.ilike(search_filter)
                )
            )

        # Get total count
        total = query.count()

        # Apply pagination
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }

    def get_by_id(self, db: Session, sbu_id: int):
        return db.query(SBU).filter(SBU.id == sbu_id, SBU.is_deleted == False).first()

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
            obj.is_deleted = True
            db.commit()
            return True
        return False

sbu_repo = SBURepository()
