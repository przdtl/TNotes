class BaseItemsCallbackDataMeta(type):
    def __setattr__(cls, name, value):
        if name in cls.__dict__:
            raise AttributeError('Cannot reassign members.')
        super().__setattr__(name, value)


class BaseItemsCallbackData(metaclass=BaseItemsCallbackDataMeta):
    __item_name__: str = ''

    CREATE_NEW_ITEM = 'CREATE_NEW'
    LIST_OF_ITEMS = 'LIST_OF'
    GO_BACK_FROM_CREATE_ITEM = 'GO_BACK_FROM_CREATE'
    GO_BACK_FROM_DELETE_ITEM = 'GO_BACK_FROM_DELETE'
    GO_HOME_FROM_LIST_OF_ITEMS = 'GO_HOME_FROM_LIST_OF'
    DELETE_ITEM = 'DELETE'

    def __init_subclass__(cls, **kwargs) -> None:
        if "item_name" not in kwargs:
            raise ValueError()
        cls.__item_name__ = kwargs.pop("item_name").upper()
        for attr in dir(cls):
            if callable(getattr(cls, attr)) or attr.startswith("__"): continue
            plural_ending = '' if attr[-1].lower() != 's' else 'S'
            setattr(cls, attr, getattr(cls, attr) + '_' + cls.__item_name__ + plural_ending)

        super().__init_subclass__(**kwargs)
