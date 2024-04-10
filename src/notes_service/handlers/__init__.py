from aiogram import Router
from .notes import router as n_router
from .vaults import router as v_router

router = Router()

router.include_router(v_router)
router.include_router(n_router)
