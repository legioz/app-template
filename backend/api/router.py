from fastapi import APIRouter
from api.routes import (
    auth_v1, 
)

router = APIRouter()

router.include_router(auth_v1.router, prefix='/auth')
