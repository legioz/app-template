from fastapi import APIRouter
from api.routes import (
    hello_world, 
    # auth_v1, 
    auth_v2,
)

router = APIRouter()

router.include_router(hello_world.router, prefix='/hello_world')
# router.include_router(auth_v1.router, prefix='/v1/auth')
router.include_router(auth_v2.router, prefix='/v2/auth')
