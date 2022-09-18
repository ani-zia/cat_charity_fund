from datetime import datetime
from typing import Set

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import BaseModel


async def donation_process(
    obj_in: BaseModel,
    model_from_db: BaseModel,
    session: AsyncSession
) -> BaseModel:
    while not obj_in.fully_invested:
        source_db = await session.execute(select(model_from_db).where(
            model_from_db.fully_invested == False  # noqa
        ))
        source_db = source_db.scalars().first()
        if source_db:
            obj_in, source_db = await money_distribution(obj_in, source_db)
            session.add(obj_in)
            session.add(source_db)
            await session.commit()
            await session.refresh(obj_in)
        else:
            break
    return obj_in


async def close_entity(obj_db: BaseModel) -> BaseModel:
    if obj_db.full_amount < 0:
        obj_db.invested_amount = abs(obj_db.full_amount)
    else:
        obj_db.invested_amount = -abs(obj_db.full_amount)
    obj_db.fully_invested = True
    obj_db.close_date = datetime.now()
    return obj_db


async def money_distribution(
    input_obj: BaseModel,
    db_obj: BaseModel
) -> Set[BaseModel]:
    remain_in = input_obj.full_amount + input_obj.invested_amount
    remain_db = db_obj.full_amount + db_obj.invested_amount
    if abs(remain_in) < abs(remain_db):
        db_obj.invested_amount += remain_in
        input_obj = await close_entity(input_obj)
    elif abs(remain_in) == abs(remain_db):
        await close_entity(input_obj)
        await close_entity(db_obj)
    else:
        input_obj.invested_amount += remain_db
        db_obj = await close_entity(db_obj)
    return input_obj, db_obj
