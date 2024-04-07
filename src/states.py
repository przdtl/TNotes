from aiogram.fsm.state import StatesGroup, State


class BaseStates(StatesGroup):
    start_state = State()


class VaultsStates(StatesGroup):
    list_vaults = State()
    create_vault = State()
    delete_vault = State()


class NotesStates(StatesGroup):
    list_notes = State()
    create_note = State()
    delete_note = State()
