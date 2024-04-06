import uuid
from typing import Optional

from aiogram.filters.callback_data import CallbackData


class NotesListNoteCallback(CallbackData, prefix='notes_list_note'):
    note_uuid_id: uuid.UUID


class NotesListGoToParentCallback(CallbackData, prefix='notes_list_go_to_parent_callback'):
    parent_uuid_id: Optional[uuid.UUID]
