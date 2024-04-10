from aiogram import Router

from .vaults import router as v_router
from .notes import router as n_router

router = Router()

router.include_router(v_router)
router.include_router(n_router)
