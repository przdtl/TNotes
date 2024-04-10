import asyncio
import logging
import sys

from src.config import settings
from src.main_menu.handlers import router as commands_router
from src.notes_service.handlers import router as notes_handlers_router
from src.notes_service.queries import router as notes_queries_router


async def main() -> None:
    settings.dp.include_router(notes_handlers_router)
    settings.dp.include_router(notes_queries_router)
    settings.dp.include_router(commands_router)
    await settings.dp.start_polling(settings.bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
