from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_active,
                                check_charity_project_exists,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.crud.charityproject import (create_charity_project,
                                     delete_charity_project,
                                     read_all_projects_from_db,
                                     update_charity_project)
from app.schemas.charityproject import (CharityProjectCreate,
                                        CharityProjectDB,
                                        CharityProjectUpdate)


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    new_project = await create_charity_project(charity_project, session)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_active(project_id, session)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Мало денег'
        )
    charity_project = await update_charity_project(charity_project,
                                                   obj_in,
                                                   session)
    return charity_project


@router.get('/', response_model=List[CharityProjectDB])
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    charity_projects = await read_all_projects_from_db(session)
    return charity_projects


@router.delete('/{project_id}', response_model=CharityProjectDB)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(project_id, session)
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Уже есть денежки'
        )
    charity_project = await delete_charity_project(charity_project, session)
    return charity_project
