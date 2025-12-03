from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine
from app.routers import auth, users, protected
# Ensure all models are imported so SQLAlchemy discovers them
from app.models import User, Role, Permission, RefreshToken

app = FastAPI(title="RBAC FastAPI (JWT + Refresh)")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(protected.router, prefix="/protected", tags=["protected"])

@app.get("/")
def root():
    return {"msg": "RBAC FastAPI"}
