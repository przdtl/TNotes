from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.list_items.service import AbstractItemsListService
from src.notes_service.keyboards import VaultsListKeyboard, NotesListKeyboard
from src.notes_service.models import PointType
from src.notes_service.repositories import VaultRepository, NoteRepository
from src.notes_service.states import VaultsStates, NotesStates
from src.user.repository import UserRepository
from src.user.service import UserService


class VaultsListService(AbstractItemsListService):
    keyboard = VaultsListKeyboard
    repository = VaultRepository
    parent_repository = UserRepository
    list_items_states_group = VaultsStates
    name_of_list_of_relatives = 'vaults'

    @classmethod
    async def create_new_item(cls, message: Message, state: FSMContext, **kwargs):
        chat_id = message.chat.id
        vault_name = message.text
        user = await UserService(UserRepository).get_or_create_user(chat_id=chat_id)
        new_item_data = {'user_id': user.id, 'name': vault_name}
        list_items_data = {'user_id': user.id}
        new_vault = await super().create_new_item(message, state, new_item_data=new_item_data,
                                                  list_items_data=list_items_data)
        new_item_data = {'name': vault_name, 'point_type': PointType.FOLDER, 'vault_id': new_vault.id}
        await NotesListService.create_new_item(message, state, new_item_data=new_item_data, is_list_item=False)

    @classmethod
    async def delete_item(cls, message: Message, state: FSMContext, is_list_item: bool = True, **kwargs):
        chat_id = message.chat.id
        vault_name = message.text
        user = await UserService(UserRepository).get_or_create_user(chat_id=chat_id)
        await super().delete_item(message, state, is_list_item, name=vault_name, user_id=user.id)


class NotesListService(AbstractItemsListService):
    keyboard = NotesListKeyboard
    repository = NoteRepository
    parent_repository = VaultRepository
    list_items_states_group = NotesStates
    name_of_list_of_relatives = 'points'
