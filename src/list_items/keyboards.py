from abc import ABC
from typing import Type, Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.list_items.callback_filters import (ItemsListItemClickCallbackFilter, ItemsListRightPageClickCallbackFilter,
                                             ItemsListLeftPageClickCallbackFilter)
from src.list_items.enums import BaseItemsCallbackData


class AbstractItemsListKeyboard(ABC):
    items_list_item_click_callback_filter: Type[ItemsListItemClickCallbackFilter] = None
    items_list_right_page_click_callback_filter: Type[ItemsListRightPageClickCallbackFilter] = None
    items_list_left_page_click_callback_filter: Type[ItemsListLeftPageClickCallbackFilter] = None
    base_items_callback_data: Type[BaseItemsCallbackData] = None

    @classmethod
    def get_full_items_list_kb(cls,
                               items: list,
                               page: int,
                               items_width: int = 2,
                               ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.attach(InlineKeyboardBuilder.from_markup(cls._get_kb_before_items_list(items=items)))
        builder.attach(InlineKeyboardBuilder.from_markup(cls.__items_list(items, page, items_width)))
        builder.attach(InlineKeyboardBuilder.from_markup(
            cls._get_kb_after_items_list_and_before_interface(items=items)))
        builder.attach(InlineKeyboardBuilder.from_markup(cls.__get_items_list_interface()))
        builder.attach(InlineKeyboardBuilder.from_markup(cls._get_kb_after_interface(items=items)))
        return builder.as_markup()

    @classmethod
    def __items_list(cls, items: list, page: int, items_width: int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        keyboard: list[InlineKeyboardButton] = [
            InlineKeyboardButton(text=item.name,
                                 callback_data=cls.items_list_item_click_callback_filter(item_uuid_id=item.id).pack())
            for item in items
        ]
        builder.row(
            width=items_width,
            *keyboard,
        )
        items_markup = InlineKeyboardMarkup(inline_keyboard=[])
        builder.attach(InlineKeyboardBuilder.from_markup(items_markup))
        builder.attach(InlineKeyboardBuilder.from_markup(cls.__get_page_buttons(current_page=page)))
        return builder.as_markup()

    @classmethod
    def _get_kb_before_items_list(cls, items: list,
                                  keyboard: Optional[list[list[InlineKeyboardButton]]] = None) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=keyboard if keyboard else [[InlineKeyboardButton]])

    @classmethod
    def _get_kb_after_items_list_and_before_interface(cls, items: list,
                                                      keyboard: Optional[list[list[InlineKeyboardButton]]] = None
                                                      ) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=keyboard if keyboard else [[InlineKeyboardButton]])

    @classmethod
    def _get_kb_after_interface(cls, items: list,
                                keyboard: Optional[list[list[InlineKeyboardButton]]] = None) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=keyboard if keyboard else [[InlineKeyboardButton]])

    @classmethod
    def __get_page_buttons(cls, current_page: int):
        left_button = InlineKeyboardButton(text='⬅️',
                                           callback_data=cls.items_list_left_page_click_callback_filter(size=10,
                                                                                                        page=current_page).pack())
        right_button = InlineKeyboardButton(text='➡️',
                                            callback_data=cls.items_list_right_page_click_callback_filter(size=10,
                                                                                                          page=current_page).pack())
        return InlineKeyboardMarkup(inline_keyboard=[[left_button, right_button]])

    @classmethod
    def __get_items_list_interface(cls):
        create_button = InlineKeyboardButton(text='➕', callback_data=cls.base_items_callback_data.CREATE_NEW_ITEM)
        delete_button = InlineKeyboardButton(text='➖', callback_data=cls.base_items_callback_data.DELETE_ITEM)
        home_button = InlineKeyboardButton(text='🏠',
                                           callback_data=cls.base_items_callback_data.GO_HOME_FROM_LIST_OF_ITEMS)
        return InlineKeyboardMarkup(inline_keyboard=[[create_button, delete_button, home_button]])
