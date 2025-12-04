from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.user import UserCreate
from app.repositories.user_repository import UserRepository

router = APIRouter()

@router.post("/", tags=["users"])
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    u = repo.create_user(user_in)
    return {
        "id": u.id,
        "email": u.email,
        "roles": [r.name for r in u.roles]
    }
