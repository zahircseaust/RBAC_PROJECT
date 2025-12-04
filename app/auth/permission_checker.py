from fastapi import Depends, HTTPException, status
from app.auth.jwt import get_current_user

def require_permission(permission: str):
    def wrapper(current_user = Depends(get_current_user)):
        user_permissions = []

        for role in current_user.roles:
            for perm in role.permissions:
                user_permissions.append(perm.name)

        if permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission"
            )
        return current_user
    return wrapper
