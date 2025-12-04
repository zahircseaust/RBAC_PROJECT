from sqlalchemy import Column, Integer, String, Text
from app.database.base import Base

class SBU(Base):
    __tablename__ = "sbus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
