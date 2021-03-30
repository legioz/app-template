from fastapi import APIRouter, Request, Depends
from core.config import templates, AuthJWT
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get('/', response_class=HTMLResponse, name='hello_world:helloWorld')
async def helloWorld(request: Request):
    return templates.TemplateResponse('hello_world/hello_world.html', {'request': request})


@router.get('/login', response_class=HTMLResponse)
async def loginForm(request: Request):
    return templates.TemplateResponse('auth/login.html', {'request': request})


@router.get('/protected')
def protected(Authorize: AuthJWT = Depends()):
    """
    We do not need to make any changes to our protected endpoints. They
    will all still function the exact same as they do when sending the
    JWT in via a headers instead of a cookies
    """
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


@router.get('/{nome}', response_class=HTMLResponse, name='hello_world:helloWorldName')
async def helloWorldName(request: Request, nome):
    return templates.TemplateResponse('hello_world/hello_world.html', {'request': request})
