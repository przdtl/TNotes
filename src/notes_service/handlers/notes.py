from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.notes_service.services import NotesListService
from src.notes_service.states import NotesStates

router = Router()


# Создаёт новую папку
@router.message(
    StateFilter(NotesStates.create_item),
)
async def create_new_note_handler(message: Message, state: FSMContext):
    await NotesListService.create_new_item(message, state, chat_id=message.chat.id,
                                           vault_name=message.text)


# Удаление папки по её имени
@router.message(
    StateFilter(NotesStates.delete_item),
)
async def delete_note_handler(message: Message, state: FSMContext):
    await NotesListService.delete_item(message, state, chat_id=message.chat.id)
