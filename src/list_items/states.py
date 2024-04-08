from aiogram.fsm.state import StatesGroup, State


class ListItemsStatesGroup(StatesGroup):
    list_items = State()
    create_item = State()
    delete_item = State()

    def __init_subclass__(cls, **kwargs):
        for attr in dir(cls):
            if not isinstance(getattr(cls, attr), State): continue
            setattr(cls, attr, State(state=attr, group_name=cls.__name__))
        return super().__init_subclass__(**kwargs)
