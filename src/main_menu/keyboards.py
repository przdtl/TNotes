from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.notes_service.enums import VaultsCallbackData


# from src.notes_service.services import VaultsListService


class MainMenuKeyboards:

    def __init__(self):
        self.__main_menu_keyboard = None

    def main_menu_keyboard(self) -> InlineKeyboardMarkup:
        if not self.__main_menu_keyboard:
            menus_button: InlineKeyboardButton = InlineKeyboardButton(text='Список меню📋',
                                                                      callback_data=VaultsCallbackData.LIST_OF_ITEMS)
            keyboard: list[list[InlineKeyboardButton]] = [[menus_button]]
            self.__main_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

        return self.__main_menu_keyboard


main_menu_keyboards = MainMenuKeyboards()
