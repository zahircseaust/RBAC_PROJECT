from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.dependencies import get_current_user
router = APIRouter()

@router.get("/me")
def me(current=Depends(get_current_user)):
    return {"email": current["email"], "roles": current["roles"]}

@router.get("/admin")
def admin_route(current=Depends(get_current_user)):
    if "admin" not in current.get("roles", []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Require admin role")
    return {"msg": "admin content"}
