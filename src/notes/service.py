from typing import Type

from src.repository import AbstractRepository


class NoteService:
    def __init__(self, notes_repo: Type[AbstractRepository]):
        self.notes_repo = notes_repo()

    async def get_rows_count(self):
        return await self.notes_repo.get_count()

