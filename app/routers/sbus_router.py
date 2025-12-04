from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.sbu import SBUCreate, SBUUpdate, SBUOut
from app.services.sbu_service import sbu_service
from app.auth.permission_checker import require_permission

router = APIRouter(
    prefix="/sbus",
    tags=["SBUs"]
)


# -----------------------------
# LIST SBUs
# -----------------------------
@router.get(
    "/",
    response_model=list[SBUOut],
    dependencies=[Depends(require_permission("sbus.read"))]
)
def list_sbus(db: Session = Depends(get_db)):
    return sbu_service.list(db)


# -----------------------------
# GET SINGLE SBU
# -----------------------------
@router.get(
    "/{sbu_id}",
    response_model=SBUOut,
    dependencies=[Depends(require_permission("sbus.read"))]
)
def get_sbu(sbu_id: int, db: Session = Depends(get_db)):
    sbu = sbu_service.get(db, sbu_id)
    if not sbu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SBU not found"
        )
    return sbu


# -----------------------------
# CREATE SBU
# -----------------------------
@router.post(
    "/",
    response_model=SBUOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("sbus.create"))]
)
def create_sbu(data: SBUCreate, db: Session = Depends(get_db)):
    return sbu_service.create(db, data)


# -----------------------------
# UPDATE SBU
# -----------------------------
@router.put(
    "/{sbu_id}",
    response_model=SBUOut,
    dependencies=[Depends(require_permission("sbus.update"))]
)
def update_sbu(sbu_id: int, data: SBUUpdate, db: Session = Depends(get_db)):
    updated = sbu_service.update(db, sbu_id, data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SBU not found"
        )
    return updated


# -----------------------------
# DELETE SBU
# -----------------------------
@router.delete(
    "/{sbu_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("sbus.delete"))]
)
def delete_sbu(sbu_id: int, db: Session = Depends(get_db)):
    ok = sbu_service.delete(db, sbu_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SBU not found"
        )
    return {"message": "SBU deleted"}
