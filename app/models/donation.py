from sqlalchemy import Column, Text

from app.models.base import BaseModel


class Donation(BaseModel):
    comment = Column(Text)
