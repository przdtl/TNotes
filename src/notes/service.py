from typing import Type

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.notes.repository import NoteRepository
from src.repository import AbstractRepository
from src.states import NotesStates


class NoteService:
    def __init__(self, notes_repo: Type[AbstractRepository]):
        self.notes_repo = notes_repo()

    async def get_rows_count(self):
        return await self.notes_repo.get_count()

    @staticmethod
    async def list_notes(message: Message, state: FSMContext,
                         page_number: int = 1,
                         page_size: int = 10,
                         edit_instead_of_new: bool = True) -> None:
        await state.set_state(NotesStates.list_notes)
        notes = await NoteService(NoteRepository).get_all_vaults(chat_id=message.chat.id)
        notes = vaults[(page_number * page_size) - page_size: page_number * page_size]
        kwargs = {'text': 'Список томов', 'reply_markup': note_keyboard.vaults_list(vaults, page_number)}
        if edit_instead_of_new:
            await message.edit_text(**kwargs)
        else:
            await message.answer(**kwargs)
