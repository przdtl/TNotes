from typing import Type

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.exc import NoResultFound

from src.base.keyboards import base_keyboards
from src.database import async_session_maker
from src.notes.models import VaultPoint, PointType
from src.vaults.enums import VaultsCallbackHandlers
from src.vaults.keyboards import note_keyboard
from src.vaults.models import Vault
from src.vaults.repository import VaultRepository
from src.repository import AbstractRepository
from src.states import NoteStates
from src.user.models import User
from src.user.service import UserService
from src.user.repository import UserRepository


class VaultService:

    def __init__(self, notes_repo: Type[AbstractRepository]):
        self.notes_repo = notes_repo()

    @staticmethod
    async def get_all_vaults(chat_id: int) -> list[Vault]:
        user: User = await UserService(UserRepository).get_or_create_user(chat_id=chat_id)
        async with async_session_maker() as session:
            user = await session.merge(user)
            items = await user.awaitable_attrs.vaults
            return items

    async def get_rows_count(self):
        return await self.notes_repo.get_count()

    async def create_new_vault(self, chat_id: int, vault_name: str) -> Vault:
        user: User = await UserService(UserRepository).get_or_create_user(chat_id=chat_id)
        async with async_session_maker() as session:
            user = await session.merge(user)
            user_uuid_id = user.id
            vault = Vault(name=vault_name, user_id=user_uuid_id)
            session.add(vault)
            await session.commit()
            vault = await self.notes_repo.get(name=vault_name, user_id=user_uuid_id)
            root_point = VaultPoint(name=vault_name, point_type=PointType.FOLDER, vault_id=vault.id)
            session.add(root_point)
            await session.commit()
            return vault

    @staticmethod
    async def list_vaults(message: Message, state: FSMContext,
                          page_number: int = 1,
                          page_size: int = 10,
                          edit_instead_of_new: bool = True) -> None:
        await state.set_state(NoteStates.list_vaults)
        vaults = await VaultService(VaultRepository).get_all_vaults(chat_id=message.chat.id)
        vaults = vaults[(page_number * page_size) - page_size: page_number * page_size]
        kwargs = {'text': 'Список томов', 'reply_markup': note_keyboard.vaults_list(vaults, page_number)}
        if edit_instead_of_new:
            await message.edit_text(**kwargs)
        else:
            await message.answer(**kwargs)

    async def delete_vault(self, message: Message, state: FSMContext):
        user: User = await UserService(UserRepository).get_or_create_user(chat_id=message.chat.id)
        try:
            vault: Vault = await self.notes_repo.get(name=message.text, user_id=user.id)
            await self.notes_repo.delete(vault.id)
            await message.answer(f'Том "{vault.name}" был успешно удалён!')
            await self.list_vaults(message, state, edit_instead_of_new=False)

        except NoResultFound:
            await message.answer('Тома с таким именем не чуществует!')
            await message.answer(text='Введите название хранилища, которое желаете удалить',
                                 reply_markup=base_keyboards.back_keyboard(
                                     VaultsCallbackHandlers.GO_BACK_FROM_DELETE_VAULT))
