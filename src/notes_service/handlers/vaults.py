from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.notes_service.states import VaultsStates
from src.notes_service.services import VaultsListService

router = Router()


# Создаёт новый том
@router.message(
    StateFilter(VaultsStates.create_item),
)
async def create_new_vault_handler(message: Message, state: FSMContext):
    await VaultsListService.create_new_item(message, state)


# Удаление тома по его имени
@router.message(
    StateFilter(VaultsStates.delete_item),
)
async def delete_vault_handler(message: Message, state: FSMContext):
    await VaultsListService.delete_item(message, state, chat_id=message.chat.id)
