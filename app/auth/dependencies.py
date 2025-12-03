from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt import decode_token
from app.database.session import get_db
from sqlalchemy.orm import Session

bearer = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        roles = payload.get("roles", [])
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": email, "roles": roles}
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
