from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.password import get_password_hash

router = APIRouter()

@router.post("/", tags=["users"])
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    u = User(email=user_in.email, password=get_password_hash(user_in.password))
    db.add(u); db.commit()
    return {"id": u.id, "email": u.email}
