from app.models.user import User
from app.auth.dependencies import get_current_user

class ProtectedRepository:
    def get_me(self, current):
        return {"email": current["email"], "roles": current["roles"]}

    def get_admin_content(self, current):
        if "admin" not in current.get("roles", []):
            return None
        return {"msg": "admin content"}
