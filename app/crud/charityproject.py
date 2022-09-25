from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charityproject import (CharityProjectCreate,
                                        CharityProjectUpdate)


class CRUDCharityProject(CRUDBase):

    async def get_id_by_name(
        self,
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
        self,
        project_id: int,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        db_project = await session.execute(
            select(CharityProject).where(
                CharityProject.id == project_id
            )
        )
        return db_project.scalars().first()

    async def create_project(
            self,
            obj_in: CharityProjectCreate,
            session: AsyncSession,
    ) -> CharityProject:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update_project(
        self,
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

    async def remove_project(
        self,
        db_obj: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        await session.delete(db_obj)
        await session.commit()
        return db_obj


charityproject_crud = CRUDCharityProject(CharityProject)
