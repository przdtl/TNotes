from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.notes.callback_filters import NotesListGoToParentCallback, NotesListNoteCallback
from src.notes.models import PointType, VaultPoint
from src.vaults.callback_filters import VaultsListPageCallback
from src.notes.enums import NoteCallbackHandlers


class NotesKeyboards:
    def __init__(self):
        self.__notes_list_interface_keyboard = None

    def notes_list(self, notes: list[VaultPoint], parent_folder: VaultPoint, page: int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        keyboard: list[InlineKeyboardButton] = [
            InlineKeyboardButton(
                text=note.name + f'[{"Папка" if note.point_type == PointType.FOLDER else "Сообщение"}]',
                callback_data=NotesListNoteCallback(vault_uuid_id=note.id).pack())
            for note in notes
        ]
        builder.row(
            width=1,
            *keyboard,
        )
        notes_markup = InlineKeyboardMarkup(inline_keyboard=[])
        builder.attach(InlineKeyboardBuilder.from_markup(notes_markup))
        builder.row(
            InlineKeyboardButton(text='⏮️',
                                 callback_data=VaultsListPageCallback(is_next=False, size=10, page=page).pack()),
            InlineKeyboardButton(text='⏭️',
                                 callback_data=VaultsListPageCallback(is_next=True, size=10, page=page).pack())
        )
        builder.attach(InlineKeyboardBuilder.from_markup(self.__get_notes_list_interface()))
        builder.add(InlineKeyboardButton(text="Вернуться обратно⏫",
                                         callback_data=NotesListGoToParentCallback(
                                             parent_uuid_id=parent_folder.parent_id).pack()))
        return builder.as_markup()

    def __get_notes_list_interface(self):
        if not self.__notes_list_interface_keyboard:
            create_button = InlineKeyboardButton(text='➕', callback_data=NoteCallbackHandlers.CREATE_NEW_FOLDER)
            delete_button = InlineKeyboardButton(text='➖', callback_data=NoteCallbackHandlers.DELETE_FOLDER)
            home_button = InlineKeyboardButton(text='🏠', callback_data=NoteCallbackHandlers.GO_HOME_FROM_NOTES_LIST)
            self.__notes_list_interface_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[create_button, delete_button, home_button]])

        return self.__notes_list_interface_keyboard
