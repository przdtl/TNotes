from abc import ABC
from typing import Type, Any

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.exc import NoResultFound

from src.base.keyboards import base_keyboards
from src.list_items.keyboards import AbstractItemsListKeyboard
from src.list_items.states import ListItemsStatesGroup
from src.main_menu.keyboards import main_menu_keyboards
from src.repository import AbstractRepository
from src.states import BaseStates


class AbstractItemsListService(ABC):
    keyboard: Type[AbstractItemsListKeyboard] = None
    repository: Type[AbstractRepository] = None
    parent_repository: Type[AbstractRepository] = None
    list_items_states_group: Type[ListItemsStatesGroup] = None
    name_of_list_of_relatives: str = None

    @classmethod
    async def get_rows_count(cls):
        return await cls.repository.get_count()

    @classmethod
    async def get_all_items(cls, **kwargs) -> list[Any]:
        return await cls.repository.get_all(**kwargs)

    @classmethod
    async def create_new_item(cls, message: Message, state: FSMContext,
                              new_item_data: dict = None,
                              list_items_data: dict = None,
                              is_list_item: bool = True):
        new_vault = await cls.repository.insert(**new_item_data)
        if is_list_item and list_items_data:
            await cls.list_items(message, state, edit_instead_of_new=False, **list_items_data)
        return new_vault

    @classmethod
    async def list_items(cls,
                         message: Message,
                         state: FSMContext,
                         page_number: int = 1,
                         page_size: int = 10,
                         edit_instead_of_new: bool = True,
                         **kwargs
                         ) -> None:
        await state.set_state(cls.list_items_states_group.list_items)
        items = await cls.get_all_items(**kwargs)
        items = items[(page_number * page_size) - page_size: page_number * page_size]
        items_text = {'text': 'Список ', 'reply_markup': cls.keyboard.get_full_items_list_kb(items, page_number)}
        if edit_instead_of_new:
            await message.edit_text(**items_text)
        else:
            await message.answer(**items_text)

    @classmethod
    async def delete_item(cls, message: Message, state: FSMContext, is_list_item: bool = True, **kwargs):
        try:
            item = await cls.repository.get(**kwargs)
            await cls.repository.delete(item.id)
            if is_list_item:
                await cls.list_items(message, state, edit_instead_of_new=False)

        except NoResultFound:
            await message.answer('Тома с таким именем не чуществует!')
            await message.answer(text='Введите название хранилища, которое желаете удалить',
                                 reply_markup=base_keyboards.back_keyboard(
                                     cls.keyboard.base_items_callback_data.GO_BACK_FROM_DELETE_ITEM))

    @classmethod
    async def go_home_from_items_list(cls, callback_query: CallbackQuery, state: FSMContext):
        await state.set_state(BaseStates.start_state)
        await callback_query.message.edit_text(text='Вы вернулись на главное меню',
                                               reply_markup=main_menu_keyboards.main_menu_keyboard())
        await callback_query.answer()
