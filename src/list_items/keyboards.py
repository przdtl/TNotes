from abc import ABC
from typing import Optional, Type

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.list_items.callback_filters import (ItemsListItemClickCallbackFilter, ItemsListRightPageClickCallbackFilter,
                                             ItemsListLeftPageClickCallbackFilter)


class AbstractItemsListKeyboard(ABC):
    items_list_item_click_callback_filter: Type[ItemsListItemClickCallbackFilter] = None
    items_list_right_page_click_callback_filter: Type[ItemsListRightPageClickCallbackFilter] = None
    items_list_left_page_click_callback_filter: Type[ItemsListLeftPageClickCallbackFilter] = None

    def __init__(self):
        self.__items_list_interface_keyboard = None

    def get_full_items_list_kb(self,
                               items: list,
                               page: int,
                               items_width: int = 2,
                               kb_before_items_list: list[list[InlineKeyboardButton]] = None,
                               kb_after_items_list_and_before_interface: list[list[InlineKeyboardButton]] = None,
                               kb_after_interface: list[list[InlineKeyboardButton]] = None,
                               ):
        kb_before_items_list = [[]] if not kb_before_items_list else kb_before_items_list
        kb_after_items_list_and_before_interface = [
            []] if not kb_after_items_list_and_before_interface else kb_after_items_list_and_before_interface
        kb_after_interface = [[]] if not kb_after_interface else kb_after_interface
        builder = InlineKeyboardBuilder()
        builder.attach(InlineKeyboardBuilder.from_markup(self.__get_kb_before_items_list(kb_before_items_list)))
        builder.attach(InlineKeyboardBuilder.from_markup(self.__items_list(items, page, items_width)))
        builder.attach(InlineKeyboardBuilder.from_markup(
            self.__get_kb_after_items_list_and_before_interface(kb_after_items_list_and_before_interface)))
        builder.attach(InlineKeyboardBuilder.from_markup(self.__get_items_list_interface()))
        builder.attach(InlineKeyboardBuilder.from_markup(self.__get_kb_after_interface(kb_after_interface)))

    def __items_list(self, items: list, page: int, items_width: int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        keyboard: list[InlineKeyboardButton] = [
            InlineKeyboardButton(text=item.name,
                                 callback_data=self.items_list_item_click_callback_filter(item_uuid_id=item.id).pack())
            for item in items
        ]
        builder.row(
            width=items_width,
            *keyboard,
        )
        items_markup = InlineKeyboardMarkup(inline_keyboard=[])
        builder.attach(InlineKeyboardBuilder.from_markup(items_markup))
        builder.attach(InlineKeyboardBuilder.from_markup(self.__get_page_buttons(current_page=page)))
        return builder.as_markup()

    @classmethod
    def __get_kb_before_items_list(cls, keyboard: list[list[InlineKeyboardButton]]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def __get_kb_after_items_list_and_before_interface(cls,
                                                       keyboard: list[list[InlineKeyboardButton]]
                                                       ) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def __get_kb_after_interface(cls, keyboard: list[list[InlineKeyboardButton]]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def __get_page_buttons(self, current_page: int):
        left_button = InlineKeyboardButton(text='⬅️',
                                           callback_data=self.items_list_left_page_click_callback_filter(size=10,
                                                                                                         page=current_page).pack())
        right_button = InlineKeyboardButton(text='➡️',
                                            callback_data=self.items_list_right_page_click_callback_filter(size=10,
                                                                                                           page=current_page).pack())
        return InlineKeyboardMarkup(inline_keyboard=[[left_button, right_button]])

    def __get_items_list_interface(self):
        if not self.__items_list_interface_keyboard:
            create_button = InlineKeyboardButton(text='➕', callback_data=VaultsCallbackHandlers.CREATE_NEW_VAULT)
            delete_button = InlineKeyboardButton(text='➖', callback_data=VaultsCallbackHandlers.DELETE_VAULT)
            home_button = InlineKeyboardButton(text='🏠', callback_data=VaultsCallbackHandlers.GO_HOME_FROM_VAULTS_LIST)
            self.__items_list_interface_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[create_button, delete_button, home_button]])
        return self.__items_list_interface_keyboard
