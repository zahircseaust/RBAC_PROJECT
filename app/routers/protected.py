from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.dependencies import get_current_user
from app.repositories.protected_repository import ProtectedRepository

router = APIRouter()

@router.get("/me")
def me(current=Depends(get_current_user)):
    repo = ProtectedRepository()
    return repo.get_me(current)

@router.get("/admin")
def admin_route(current=Depends(get_current_user)):
    repo = ProtectedRepository()
    result = repo.get_admin_content(current)
    if result is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Require admin role")
    return result
