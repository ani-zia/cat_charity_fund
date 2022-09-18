from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.models.charityproject import CharityProject
from app.schemas.donation import DonationCreate, DonationDB
from app.services.investment import donation_process

router = APIRouter()


@router.post('/', response_model=DonationDB)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_donation = await donation_crud.create_donation(donation, session)
    new_donation = await donation_process(new_donation, CharityProject, session)
    return new_donation


@router.get('/', response_model=List[DonationDB])
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    all_donations = await donation_crud.get_multi(session)
    return all_donations
