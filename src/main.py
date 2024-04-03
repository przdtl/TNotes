import asyncio
import logging
import sys

from src.config import settings
from src.base.handlers import router as commands_router
from src.notes.handlers import router as notes_router


async def main() -> None:
    settings.dp.include_router(notes_router)
    settings.dp.include_router(commands_router)
    await settings.dp.start_polling(settings.bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
