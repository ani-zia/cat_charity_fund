from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charityproject import CharityProject
from app.schemas.charityproject import (CharityProjectCreate,
                                        CharityProjectUpdate)


async def create_charity_project(
    new_project: CharityProjectCreate,
    session: AsyncSession
) -> CharityProject:
    new_project_data = new_project.dict()
    db_project = CharityProject(**new_project_data)
    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project


async def get_project_id_by_name(
    project_name: str,
    session: AsyncSession
) -> Optional[int]:
    db_project_id = await session.execute(
        select(CharityProject.id).where(
            CharityProject.name == project_name
        )
    )
    return db_project_id.scalars().first()


async def get_project_by_id(
    project_id: int,
    session: AsyncSession,
) -> Optional[CharityProject]:
    db_project = await session.execute(
        select(CharityProject).where(
            CharityProject.id == project_id
        )
    )
    return db_project.scalars().first()


async def update_charity_project(
    db_obj: CharityProject,
    obj_in: CharityProjectUpdate,
    session: AsyncSession,
) -> CharityProject:
    db_obj_data = jsonable_encoder(db_obj)
    update_data = obj_in.dict(exclude_unset=True)
    for field in db_obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def read_all_projects_from_db(
    session: AsyncSession,
) -> List[CharityProject]:
    db_objs = await session.execute(select(CharityProject))
    return db_objs.scalars().all()


async def delete_charity_project(
    db_obj: CharityProject,
    session: AsyncSession,
) -> CharityProject:
    await session.delete(db_obj)
    await session.commit()
    return db_obj
