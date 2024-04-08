from abc import ABC
from typing import Type, Any

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.exc import NoResultFound

from src.base.keyboards import base_keyboards
from src.list_items.keyboards import AbstractItemsListKeyboard
from src.list_items.states import ListItemsStatesGroup
from src.repository import AbstractRepository


class AbstractItemsListService(ABC):
    keyboard: Type[AbstractItemsListKeyboard] = None
    repository: Type[AbstractRepository] = None
    parent_repository: Type[AbstractRepository] = None
    list_items_states_group: Type[ListItemsStatesGroup] = None
    name_of_list_of_relatives: str = None

    async def get_rows_count(self):
        return await self.repository().get_count()

    async def get_all_items(self, **kwargs) -> list[Any]:
        parent_object = await self.parent_repository.get(**kwargs)
        return await self.parent_repository().get_related_objects(parent_object.id, self.name_of_list_of_relatives)

    async def create_new_item(self, **kwargs):
        return await self.repository().insert(**kwargs)

    async def list_items(self, message: Message, state: FSMContext,
                         page_number: int = 1,
                         page_size: int = 10,
                         edit_instead_of_new: bool = True
                         ) -> None:
        await state.set_state(self.list_items_states_group.list_items)
        items = await self.get_all_items()
        items = items[(page_number * page_size) - page_size: page_number * page_size]
        kwargs = {'text': 'Список ', 'reply_markup': self.keyboard.get_full_items_list_kb(items, page_number)}
        if edit_instead_of_new:
            await message.edit_text(**kwargs)
        else:
            await message.answer(**kwargs)

    async def delete_item(self, message: Message, state: FSMContext, **kwargs):
        try:
            item = await self.repository().get(**kwargs)
            await self.repository().delete(item.id)
            await message.answer(f'"{item.name}" был успешно удалён!')
            await self.list_items(message, state, edit_instead_of_new=False)

        except NoResultFound:
            await message.answer('Тома с таким именем не чуществует!')
            await message.answer(text='Введите название хранилища, которое желаете удалить',
                                 reply_markup=base_keyboards.back_keyboard(
                                     self.keyboard.base_items_callback_data.GO_BACK_FROM_DELETE_ITEM))
