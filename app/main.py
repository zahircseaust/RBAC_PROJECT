from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine
from app.routers import auth, users, protected, sbus_router
# Ensure all models are imported so SQLAlchemy discovers them
from app.models import User, Role, Permission, RefreshToken
from app.models.sbus import SBU

app = FastAPI(title="BTI-Backend")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(protected.router, prefix="/protected", tags=["protected"])
app.include_router(sbus_router.router, prefix="/sbus", tags=["SBUs"])
# app.include_router(sbu_router).router, prefix="/sbus", tags=["SBUs"])

@app.get("/")
def root():
    return {"msg": "RBAC FastAPI"}
