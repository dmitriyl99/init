from fastapi import APIRouter

from app.site import home

site_router = APIRouter()
site_router.include_router(home.router, tags=['home'])
