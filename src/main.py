import asyncio
import logging
import sys

from src.config import settings
from src.handlers.commands import router as commands_router


async def main() -> None:
    settings.dp.include_router(commands_router)
    await settings.dp.start_polling(settings.bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
