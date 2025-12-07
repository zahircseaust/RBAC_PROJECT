from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config.settings import settings
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.exceptions import UnauthorizedException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


bearer_scheme = HTTPBearer()

def create_access_token(subject: str, roles: list, expires_minutes: int = None):
    expires = datetime.utcnow() + timedelta(minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "roles": roles, "exp": expires}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise UnauthorizedException(message="Invalid token")

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise UnauthorizedException(message="Invalid token payload")

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise UnauthorizedException(message="User not found")
        return user
    except JWTError:
        raise UnauthorizedException(message="Invalid or expired token")
