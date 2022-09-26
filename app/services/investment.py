from datetime import datetime
from typing import Set

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import BaseModel


async def donation_process(
    obj_in: BaseModel,
    model_db: BaseModel,
    session: AsyncSession
) -> BaseModel:
    source_db_all = await session.execute(select(model_db).where(
       model_db.fully_invested == False  # noqa
    ).order_by(model_db.create_date))
    source_db_all = source_db_all.scalars().all()
    for source_db in source_db_all:
        obj_in, source_db = await money_distribution(obj_in,
                                                     source_db)
        session.add(obj_in)
        session.add(source_db)
    await session.commit()
    await session.refresh(obj_in)
    return obj_in


async def close_entity(obj_db: BaseModel) -> BaseModel:
    obj_db.invested_amount = obj_db.full_amount
    obj_db.fully_invested = True
    obj_db.close_date = datetime.now()
    return obj_db


async def money_distribution(
    obj_in: BaseModel,
    obj_db: BaseModel
) -> Set[BaseModel]:
    rem_obj_in = obj_in.full_amount - obj_in.invested_amount
    rem_obj_db = obj_db.full_amount - obj_db.invested_amount
    if rem_obj_in > rem_obj_db:
        obj_in.invested_amount += rem_obj_db
        obj_db = await close_entity(obj_db)
    elif rem_obj_in == rem_obj_db:
        obj_in = await close_entity(obj_in)
        obj_db = await close_entity(obj_db)
    else:
        obj_db.invested_amount += rem_obj_in
        obj_in = await close_entity(obj_in)
    return obj_in, obj_db
