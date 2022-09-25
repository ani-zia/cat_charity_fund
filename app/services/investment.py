from datetime import datetime
from typing import Set

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import BaseModel


async def donation_process(
    obj_in_donat: BaseModel,
    model_db_proj: BaseModel,
    session: AsyncSession
) -> BaseModel:
    while not obj_in_donat.fully_invested:
        source_db = await session.execute(select(model_db_proj).where(
            model_db_proj.fully_invested == False  # noqa
        ))
        source_db = source_db.scalars().first()
        if source_db:
            obj_in_donat, source_db = await money_distribution(obj_in_donat,
                                                               source_db)
            session.add(obj_in_donat)
            session.add(source_db)
            await session.commit()
            await session.refresh(obj_in_donat)
        else:
            break
    return obj_in_donat


async def accepter_process(
    obj_in_proj: BaseModel,
    model_db_donat: BaseModel,
    session: AsyncSession
) -> BaseModel:
    while not obj_in_proj.fully_invested:
        source_db = await session.execute(select(model_db_donat).where(
            model_db_donat.fully_invested == False  # noqa
        ))
        source_db = source_db.scalars().first()
        if source_db:
            obj_in_proj, source_db = await money_distribution(obj_in_proj,
                                                              source_db)
            session.add(obj_in_proj)
            session.add(source_db)
            await session.commit()
            await session.refresh(obj_in_proj)
        else:
            break
    return obj_in_proj


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
