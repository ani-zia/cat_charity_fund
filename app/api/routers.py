from fastapi import APIRouter

from app.api.endpoints import charityproject_router, donation_router


main_router = APIRouter()

main_router.include_router(charityproject_router,
                           prefix='/charity_project',
                           tags=['charity_projects'])
main_router.include_router(donation_router,
                           prefix='/donation',
                           tags=['donations'])
