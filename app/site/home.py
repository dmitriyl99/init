from fastapi import APIRouter, Request

from app.core.templates import response_with_template


router = APIRouter()


@router.get('/')
def home_page(request: Request):
    return response_with_template(request, 'home.html')
