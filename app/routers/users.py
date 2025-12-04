from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.password import get_password_hash
from app.models.role import Role

router = APIRouter()


@router.post("/", tags=["users"])
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    u = User(
        email=user_in.email,
        password=get_password_hash(user_in.password),
    )
    if user_in.role_names:
        roles = (
            db.query(Role)
            .filter(Role.name.in_(user_in.role_names))
            .all()
        )
        u.roles = roles         

    db.add(u)
    db.commit()
    db.refresh(u)

    return {
        "id": u.id,
        "email": u.email,
        "roles": [r.name for r in u.roles]
    }
