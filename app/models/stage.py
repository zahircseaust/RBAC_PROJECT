from sqlalchemy import Column, Integer, String, Text, Boolean
from app.database.base import Base


class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    order_no = Column(Integer)
    status = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
