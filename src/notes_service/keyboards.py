from typing import Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.list_items.keyboards import AbstractItemsListKeyboard
from src.notes_service.callback_filters import (VaultsListVaultClickCallbackFilter,
                                                VaultsListRightPageClickCallbackFilter,
                                                VaultsListLeftPageClickCallbackFilter, NotesListNoteClickCallbackFilter,
                                                NotesListRightPageClickCallbackFilter,
                                                NotesListLeftPageClickCallbackFilter)
from src.notes_service.enums import (VaultsCallbackData, NotesCallbackData)


class VaultsListKeyboard(AbstractItemsListKeyboard):
    items_list_item_click_callback_filter = VaultsListVaultClickCallbackFilter
    items_list_right_page_click_callback_filter = VaultsListRightPageClickCallbackFilter
    items_list_left_page_click_callback_filter = VaultsListLeftPageClickCallbackFilter
    base_items_callback_data = VaultsCallbackData


class NotesListKeyboard(AbstractItemsListKeyboard):
    items_list_item_click_callback_filter = NotesListNoteClickCallbackFilter
    items_list_right_page_click_callback_filter = NotesListRightPageClickCallbackFilter
    items_list_left_page_click_callback_filter = NotesListLeftPageClickCallbackFilter
    base_items_callback_data = NotesCallbackData

    @classmethod
    def _get_kb_after_interface(cls,
                                items: list,
                                keyboard: Optional[list[list[InlineKeyboardButton]]] = None) -> InlineKeyboardMarkup:

        keyborad = []
        return super()._get_kb_after_interface(items, keyborad)


    @classmethod
    def