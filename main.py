from fastapi import FastAPI
from core.config import PROJECT_NAME, DEBUG
from api.router import router as api_router
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from core.config import SECRET_KEY

VERSION = '20210218'

app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(api_router, prefix='/api')
