from enum import Enum


class NoteCallbackHandlers(str, Enum):
    CREATE_NEW_FOLDER = 'CREATE_NEW_FOLDER'
    DELETE_FOLDER = 'DELETE_FOLDER'
    GO_HOME_FROM_NOTES_LIST = 'GO_HOME_FROM_NOTES_LIST'
