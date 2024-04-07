import enum
from typing import Optional


class BaseItemsCallbackData:
    __item_name__: str = ''

    CREATE_NEW = 'CREATE_NEW_' + __item_name__
    LIST_OF = 'LIST_OF_' + __item_name__
    GO_BACK_FROM_CREATE_ = 'GO_BACK_FROM_CREATE_' + __item_name__
    GO_HOME_FROM_LIST_OF = 'GO_HOME_FROM_LIST_OF_' + __item_name__
    DELETE = 'DELETE_' + __item_name__
    GO_BACK_FROM_DELETE = 'GO_BACK_FROM_DELETE_' + __item_name__


class VaultsListCallbackData(BaseItemsCallbackData):
    __item_name__ = 'vault'

    def __init__(self):
        super().__init__()

    @classmethod
    def pr(cls):
        print([func for func in dir(cls) if not callable(getattr(cls, func)) and not func.startswith("__")])


print(VaultsListCallbackData.LIST_OF)
print(VaultsListCallbackData.LIST_OF)

a = VaultsListCallbackData()
