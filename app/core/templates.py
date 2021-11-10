from typing import Optional

from fastapi import Request
from fastapi.templating import Jinja2Templates

_template_engine = Jinja2Templates(directory='resources/templates')


def response_with_template(
        request: Request,
        template_name: str,
        context: Optional[dict] = None,
        status_code: int = 200):
    if context is None:
        context = {}
    context['request'] = request
    return _template_engine.TemplateResponse(template_name, context=context, status_code=status_code)
