from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from src.base.enums import BaseHandlers
from src.notes.enums import NoteHandlers, NoteCallbackHandlers


class BaseKeyboards:

    def __init__(self):
        self.__main_menu_keyboard = None
        self.__back_keyboard = None

    def main_menu_keyboard(self) -> InlineKeyboardMarkup:
        if not self.__main_menu_keyboard:
            menus_button: InlineKeyboardButton = InlineKeyboardButton(text='Список меню📋',
                                                                      callback_data=NoteCallbackHandlers.VAULTS_LIST)
            keyboard: list[list[InlineKeyboardButton]] = [[menus_button]]
            self.__main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        return self.__main_menu_keyboard

    def back_keyboard(self, callback_data: str) -> InlineKeyboardMarkup:
        if not self.__back_keyboard:
            keyboard: list[list[InlineKeyboardButton]] = [
                [InlineKeyboardButton(text=BaseHandlers.Back, callback_data=callback_data)]]
            self.__back_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        return self.__back_keyboard


base_keyboards = BaseKeyboards()
