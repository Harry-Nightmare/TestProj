from fastapi import APIRouter

from . import (
    auth,
    messages,
)


router = APIRouter()
router.include_router(auth.router)
router.include_router(messages.router)
