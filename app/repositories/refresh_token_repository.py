from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken
from datetime import datetime

class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, token: str, user_id: int, expires_at: datetime):
        rt = RefreshToken(token=token, user_id=user_id, expires_at=expires_at)
        self.db.add(rt)
        self.db.commit()
        return rt

    def get_by_token(self, token: str):
        return self.db.query(RefreshToken).filter(RefreshToken.token == token).first()

    def delete(self, token: str):
        rt = self.get_by_token(token)
        if rt:
            self.db.delete(rt)
            self.db.commit()
        return rt
