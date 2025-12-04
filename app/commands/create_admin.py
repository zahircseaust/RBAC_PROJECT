from app.database.session import SessionLocal, engine
from app.database.base import Base
from app.models.role import Role
from app.models.permission import Permission
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.auth.password import get_password_hash
from app.config.settings import settings

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    try:
        admin = db.query(Role).filter(Role.name=='admin').first()
        if not admin:
            admin = Role(name='admin'); db.add(admin)
        manager = db.query(Role).filter(Role.name=='manager').first()
        if not manager:
            manager = Role(name='manager'); db.add(manager)
        viewer = db.query(Role).filter(Role.name=='viewer').first()
        if not viewer:
            viewer = Role(name='viewer'); db.add(viewer)
        db.commit()

        perms = [
            'users.create', 'users.read', 'users.update', 'users.delete',
            'roles.manage',
            'sbus.create', 'sbus.read', 'sbus.update', 'sbus.delete',
            'stages.create', 'stages.read', 'stages.update', 'stages.delete'
        ]
        for pname in perms:
            p = db.query(Permission).filter(Permission.name==pname).first()
            if not p:
                p = Permission(name=pname); db.add(p)
        db.commit()

        admin = db.query(Role).filter(Role.name=='admin').first()
        if admin:
            all_perms = db.query(Permission).all()
            admin.permissions = all_perms
            db.commit()

        admin_user = db.query(User).filter(User.email==settings.ADMIN_EMAIL).first()
        if not admin_user:
            u = User(email=settings.ADMIN_EMAIL, password=get_password_hash(settings.ADMIN_PASSWORD))
            u.roles = [admin]
            db.add(u)
            db.commit()
            print("Admin created:", settings.ADMIN_EMAIL)
        else:
            print("Admin exists")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
