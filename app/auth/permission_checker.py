from fastapi import Depends
from app.auth.jwt import get_current_user
from app.exceptions import ForbiddenException

def require_permission(permission: str):
    def wrapper(current_user = Depends(get_current_user)):
        user_permissions = []

        for role in current_user.roles:
            for perm in role.permissions:
                user_permissions.append(perm.name)

        if permission not in user_permissions:
            raise ForbiddenException(
                message=f"Permission '{permission}' required"
            )
        return current_user
    return wrapper
