from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.site import site_router


app = FastAPI(
    title=settings.PROJECT_NAME
)

app.mount('/static', StaticFiles(directory='resources/assets'), name='static')

app.include_router(site_router)
