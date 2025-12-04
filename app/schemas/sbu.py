from pydantic import BaseModel
from typing import Optional, List


class SBUSchemaBase(BaseModel):
    name: str
    description: Optional[str] = None


class SBUCreate(SBUSchemaBase):
    pass


class SBUUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class SBUOut(SBUSchemaBase):
    id: int

    class Config:
        from_attributes = True


class SBUPaginatedResponse(BaseModel):
    items: List[SBUOut]
    total: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True
