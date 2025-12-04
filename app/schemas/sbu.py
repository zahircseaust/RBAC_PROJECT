from pydantic import BaseModel
from typing import Optional

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
