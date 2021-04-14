from fastapi import FastAPI, Request
from api.router import router as api_router
from app.router import router as app_router
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from core.config import (PROJECT_NAME, DEBUG,
                        SECRET_KEY, OPENAPI_URL,
                        DOCS_URL, REDOCS_URL)

VERSION = '0.0.1'

app = FastAPI(title=PROJECT_NAME, debug=DEBUG, 
            version=VERSION, docs_url=DOCS_URL,
            redoc_url=REDOCS_URL, open_api_url=OPENAPI_URL)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(api_router, prefix='/api')
app.include_router(app_router)
