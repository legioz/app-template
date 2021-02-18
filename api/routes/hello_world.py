from fastapi import APIRouter, Request
from core.config import templates
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get('/', response_class=HTMLResponse, name='hello_world:helloWorld')
async def helloWorld(request: Request):
    return templates.TemplateResponse('hello_world/hello_world.html', {'request': request})


@router.get('/login', response_class=HTMLResponse)
async def loginForm(request: Request):
    return templates.TemplateResponse('auth/login.html', {'request': request})


@router.get('/{nome}', response_class=HTMLResponse, name='hello_world:helloWorldName')
async def helloWorldName(request: Request, nome):
    return templates.TemplateResponse('hello_world/hello_world.html', {'request': request})

