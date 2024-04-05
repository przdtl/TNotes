from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.notes.callback_filters import VaultsListVaultCallback, VaultsListPageCallback
from src.notes.enums import NoteCallbackHandlers
from src.notes.models import Vault


class NoteKeyboards:

    def __init__(self):
        self.__vaults_list_interface_keyboard = None

    def vaults_list(self, vaults: list[Vault], page: int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        keyboard: list[InlineKeyboardButton] = [
            InlineKeyboardButton(text=vault.name, callback_data=VaultsListVaultCallback(vault_uuid_id=vault.id).pack())
            for vault in vaults
        ]
        builder.row(
            width=2,
            *keyboard,
        )
        vaults_markup = InlineKeyboardMarkup(inline_keyboard=[])
        builder.attach(InlineKeyboardBuilder.from_markup(vaults_markup))
        builder.row(
            InlineKeyboardButton(text='⏮️',
                                 callback_data=VaultsListPageCallback(is_next=False, size=10, page=page).pack()),
            InlineKeyboardButton(text='⏭️',
                                 callback_data=VaultsListPageCallback(is_next=True, size=10, page=page).pack())
        )
        builder.attach(InlineKeyboardBuilder.from_markup(self.__get_vaults_list_interface()))
        return builder.as_markup()

    def __get_vaults_list_interface(self):
        if not self.__vaults_list_interface_keyboard:
            create_button = InlineKeyboardButton(text='➕', callback_data=NoteCallbackHandlers.CREATE_NEW_VAULT)
            delete_button = InlineKeyboardButton(text='➖', callback_data=NoteCallbackHandlers.DELETE_VAULT)
            home_button = InlineKeyboardButton(text='🏠', callback_data=NoteCallbackHandlers.GO_HOME_FROM_VAULTS_LIST)
            self.__vaults_list_interface_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[create_button, delete_button, home_button]])
        return self.__vaults_list_interface_keyboard


note_keyboard = NoteKeyboards()
