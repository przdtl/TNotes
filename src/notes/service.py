from typing import Type, Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.exc import NoResultFound

from src.base.keyboards import base_keyboards
from src.database import async_session_maker
from src.notes.enums import NoteHandlers, NoteCallbackHandlers
from src.notes.keyboards import note_keyboard
from src.notes.models import Vault
from src.notes.repository import VaultRepository
from src.repository import AbstractRepository
from src.states import NoteStates
from src.user.models import User
from src.user.service import UserService
from src.user.repository import UserRepository


class VaultService:

    def __init__(self, notes_repo: Type[AbstractRepository]):
        self.notes_repo = notes_repo()

    @staticmethod
    async def get_all_vaults(chat_id: int, user_id: Optional[int]) -> list[Vault]:
        user: User = await UserService(UserRepository).get_or_create_user(user_id=user_id, chat_id=chat_id)
        async with async_session_maker() as session:
            user = await session.merge(user)
            items = await user.awaitable_attrs.vaults
            return items

    @staticmethod
    async def create_new_vault(user_id: int, chat_id: int, vault_name: str) -> Vault:
        user: User = await UserService(UserRepository).get_or_create_user(user_id=user_id, chat_id=chat_id)
        async with async_session_maker() as session:
            user = await session.merge(user)
            user_uuid_id = user.id
            vault = Vault(name=vault_name, user_id=user_uuid_id)
            session.add(vault)
            await session.commit()
            return vault

    @staticmethod
    async def list_vaults(message: Message, state: FSMContext, is_wo_user_id: bool = False) -> None:
        await state.set_state(NoteStates.list_vaults)
        remove_kb_message = await message.answer(text=NoteHandlers.REMOVE_BASE_KEYBOARD,
                                                 reply_markup=ReplyKeyboardRemove())
        await remove_kb_message.delete()
        user_id = message.from_user.id if not is_wo_user_id else None
        vaults = await VaultService(VaultRepository).get_all_vaults(chat_id=message.chat.id, user_id=user_id)
        await message.answer('Список томов', reply_markup=note_keyboard.vaults_list(vaults))

    async def delete_vault(self, message: Message, state: FSMContext):
        user: User = await UserService(UserRepository).get_or_create_user(user_id=message.from_user.id,
                                                                          chat_id=message.chat.id)
        try:
            vault: Vault = await self.notes_repo.get(name=message.text, user_id=user.id)
            await self.notes_repo.delete(vault.id)
            await message.answer(f'Том "{vault.name}" был успешно удалён!')
            await self.list_vaults(message, state)

        except NoResultFound:
            await message.answer('Тома с таким именем не чуществует!')
            await message.answer(text='Введите название хранилища, которое желаете удалить',
                                 reply_markup=base_keyboards.back_keyboard(
                                     NoteCallbackHandlers.GO_BACK_FROM_DELETE_VAULT))
