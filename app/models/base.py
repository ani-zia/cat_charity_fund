from datetime import datetime

from sqlalchemy import Boolean, DateTime, Column, Integer

from app.core.db import Base


class BaseModel(Base):

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None, nullable=True)
