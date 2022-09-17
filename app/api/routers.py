from fastapi import APIRouter

from app.api.endpoints import charityproject_router


main_router = APIRouter()

main_router.include_router(charityproject_router,
                           prefix='/charity_project',
                           tags=['charity_projects'])
