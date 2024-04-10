from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.base.enums import BaseHandlers


class BaseKeyboards:

    def __init__(self):
        self.__back_keyboard = None

    def back_keyboard(self, callback_data: str) -> InlineKeyboardMarkup:
        if not self.__back_keyboard:
            keyboard: list[list[InlineKeyboardButton]] = [
                [InlineKeyboardButton(text=BaseHandlers.Back, callback_data=callback_data)]]
            self.__back_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        return self.__back_keyboard


base_keyboards = BaseKeyboards()
