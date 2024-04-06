from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F

from src.vaults.enums import VaultsHandlers
from src.vaults.repository import VaultRepository
from src.vaults.service import VaultService
from src.states import NoteStates, BaseStates
from src.vaults.queries import router as queries_router

router = Router()

router.include_router(queries_router)


# Создаёт новый том
@router.message(
    StateFilter(NoteStates.create_vault),
)
async def create_new_vault_handler(message: Message, state: FSMContext):
    new_vault = await VaultService(VaultRepository).create_new_vault(chat_id=message.chat.id,
                                                                     vault_name=message.text)
    await message.answer(f'Был создан новый том с названием "{new_vault.name}"!')
    await VaultService(VaultRepository).list_vaults(message, state, edit_instead_of_new=False)


# Удаление тома по его имени
@router.message(
    StateFilter(NoteStates.delete_vault),
)
async def delete_vault_handler(message: Message, state: FSMContext):
    await VaultService(VaultRepository).delete_vault(message, state)


# Последний хендлер
@router.message(
    StateFilter(BaseStates.start_state),
)
async def handler_of_everything_handler(message: Message):
    await message.answer(f'Вы находитесь в состоянии start_state')