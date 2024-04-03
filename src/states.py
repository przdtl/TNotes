from aiogram.fsm.state import StatesGroup, State


class BaseStates(StatesGroup):
    start_state = State()


class NoteStates(StatesGroup):
    list_vaults = State()
    create_vault = State()
    delete_vault = State()
