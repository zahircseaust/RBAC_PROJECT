from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.user import UserLogin, TokenOut, TokenRefreshIn
from app.repositories.user_repository import UserRepository
from app.auth.password import verify_password
from app.auth.jwt import create_access_token
from app.models.user import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.exceptions import UnauthorizedException
from datetime import datetime, timedelta
import secrets

router = APIRouter()

@router.post("/login", response_model=TokenOut)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    refresh_repo = RefreshTokenRepository(db)
    user = user_repo.get_by_email(user_in.email)
    if not user or not verify_password(user_in.password, user.password):
        raise UnauthorizedException(message="Invalid credentials")
    role_names = [r.name for r in user.roles]
    access_token = create_access_token(user.email, role_names)
    # create refresh token
    refresh = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(days=7)
    refresh_repo.create(token=refresh, user_id=user.id, expires_at=expires)
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh}

@router.post("/refresh")
def refresh_token(body: TokenRefreshIn, db: Session = Depends(get_db)):
    refresh_repo = RefreshTokenRepository(db)
    rt = refresh_repo.get_by_token(body.refresh_token)
    if not rt or rt.expires_at < datetime.utcnow():
        raise UnauthorizedException(message="Invalid or expired refresh token")
    user = db.query(User).filter(User.id == rt.user_id).first()
    roles = [r.name for r in user.roles]
    access_token = create_access_token(user.email, roles)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(body: TokenRefreshIn, db: Session = Depends(get_db)):
    refresh_repo = RefreshTokenRepository(db)
    refresh_repo.delete(body.refresh_token)
    return {"ok": True}
