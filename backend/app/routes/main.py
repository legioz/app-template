from fastapi import APIRouter, Request, Depends
from core.config import templates
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get('/', name='main:hello_world')
async def hello_world(request: Request):
    return templates.TemplateResponse('hello_world/hello_world.html', {'request': request})


@router.get('/login', name='main:login_form')
async def login_form(request: Request):
    return templates.TemplateResponse('auth/login.html', {'request': request})


@router.get('/{nome}', name='main:hello_world_name')
async def hello_world_name(request: Request, nome):
    return templates.TemplateResponse('hello_world/hello_world.html', {'request': request})
