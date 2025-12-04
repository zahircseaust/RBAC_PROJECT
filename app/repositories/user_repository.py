from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.auth.password import get_password_hash

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user_in):
        u = User(
            email=user_in.email,
            password=get_password_hash(user_in.password),
        )
        if hasattr(user_in, 'role_names') and user_in.role_names:
            roles = (
                self.db.query(Role)
                .filter(Role.name.in_(user_in.role_names))
                .all()
            )
            u.roles = roles
        self.db.add(u)
        self.db.commit()
        self.db.refresh(u)
        return u
