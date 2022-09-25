from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationDB(DonationCreate):
    id: int
    create_date: Optional[datetime]
    user_id: Optional[int]

    class Config:
        orm_mode = True


class DonationDBFull(DonationDB):
    invested_amount: Optional[int]
    close_date: Optional[datetime]
    fully_invested: Optional[bool]
