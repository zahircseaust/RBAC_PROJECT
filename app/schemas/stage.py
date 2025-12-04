from pydantic import BaseModel
from typing import Optional, List


class StageBase(BaseModel):
    name: str
    description: Optional[str] = None
    order_no: Optional[int] = None
    status: Optional[bool] = False


class StageCreate(StageBase):
    pass


class StageUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    order_no: Optional[int] = None
    status: Optional[bool] = None


class StageOut(StageBase):
    id: int

    class Config:
        from_attributes = True


class StagePaginatedResponse(BaseModel):
    items: List[StageOut]
    total: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True
