from sqlalchemy import Column, Integer, String, Text, Boolean
from app.database.base import Base

class SBU(Base):
    __tablename__ = "sbus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    is_deleted = Column(Boolean, default=False, nullable=False)
