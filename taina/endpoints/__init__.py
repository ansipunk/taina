import fastapi

from .tokens import router as tokens_router
from .users import router as users_router

router = fastapi.APIRouter(prefix="/api")

router.include_router(tokens_router)
router.include_router(users_router)
