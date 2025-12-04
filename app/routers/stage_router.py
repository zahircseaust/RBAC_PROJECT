from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database.session import get_db
from app.schemas.stage import StageCreate, StageUpdate, StageOut, StagePaginatedResponse
from app.services.stage_service import stage_service
from app.auth.permission_checker import require_permission

router = APIRouter(
    tags=["Stages"]
)


# -----------------------------
# LIST STAGES (with pagination & search)
# -----------------------------
@router.get(
    "/",
    response_model=StagePaginatedResponse,
    dependencies=[Depends(require_permission("stages.read"))]
)
def list_stages(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name or description"),
    db: Session = Depends(get_db)
):
    return stage_service.list(db, page, page_size, search)


# -----------------------------
# GET SINGLE STAGE
# -----------------------------
@router.get(
    "/{stage_id}",
    response_model=StageOut,
    dependencies=[Depends(require_permission("stages.read"))]
)
def get_stage(stage_id: int, db: Session = Depends(get_db)):
    stage = stage_service.get(db, stage_id)
    if not stage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stage not found"
        )
    return stage


# -----------------------------
# CREATE STAGE
# -----------------------------
@router.post(
    "/",
    response_model=StageOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("stages.create"))]
)
def create_stage(data: StageCreate, db: Session = Depends(get_db)):
    return stage_service.create(db, data)


# -----------------------------
# UPDATE STAGE
# -----------------------------
@router.put(
    "/{stage_id}",
    response_model=StageOut,
    dependencies=[Depends(require_permission("stages.update"))]
)
def update_stage(stage_id: int, data: StageUpdate, db: Session = Depends(get_db)):
    updated = stage_service.update(db, stage_id, data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stage not found"
        )
    return updated


# -----------------------------
# DELETE STAGE (SOFT DELETE)
# -----------------------------
@router.delete(
    "/{stage_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("stages.delete"))]
)
def delete_stage(stage_id: int, db: Session = Depends(get_db)):
    ok = stage_service.delete(db, stage_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stage not found"
        )
    return None
