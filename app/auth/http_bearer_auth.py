from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status

security = HTTPBearer()

async def verify_bearer_token(request: Request, credentials: HTTPAuthorizationCredentials = security):
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication scheme"
        )
    return credentials.credentials
