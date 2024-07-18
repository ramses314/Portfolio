from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

from src.database.base import Base


class Timestamp(Base):
    __abstract__ = True
    created = Column(DateTime, default=func.now())
    updated = Column(DateTime, default=func.now(), onupdate=func.now())
