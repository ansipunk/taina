import fastapi

from .users import router as users_router

router = fastapi.APIRouter(prefix="/api")

router.include_router(users_router)
