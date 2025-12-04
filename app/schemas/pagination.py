from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar('T')


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 10
    search: str = None


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True
