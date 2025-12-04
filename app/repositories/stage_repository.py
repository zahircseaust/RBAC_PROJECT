from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.stage import Stage
from app.schemas.stage import StageCreate, StageUpdate


class StageRepository:

    def get_all(self, db: Session, page: int = 1, page_size: int = 10, search: str = None):
        query = db.query(Stage).filter(Stage.is_deleted == False)

        # Apply search filter
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Stage.name.ilike(search_filter),
                    Stage.description.ilike(search_filter)
                )
            )

        # Get total count
        total = query.count()

        # Apply pagination with ordering
        offset = (page - 1) * page_size
        items = query.order_by(Stage.order_no).offset(offset).limit(page_size).all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }

    def get_by_id(self, db: Session, stage_id: int):
        return db.query(Stage).filter(Stage.id == stage_id, Stage.is_deleted == False).first()

    def create(self, db: Session, obj_in: StageCreate):
        stage = Stage(**obj_in.dict())
        db.add(stage)
        db.commit()
        db.refresh(stage)
        return stage

    def update(self, db: Session, db_obj: Stage, obj_in: StageUpdate):
        data = obj_in.dict(exclude_unset=True)
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, stage_id: int):
        obj = self.get_by_id(db, stage_id)
        if obj:
            obj.is_deleted = True
            db.commit()
            return True
        return False


stage_repo = StageRepository()
