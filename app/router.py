from fastapi import APIRouter
from app.routes import (
    main, 
)

router = APIRouter()

# router.include_router(main.router)
