from abc import ABC
from typing import Type

from src.list_items.keyboards import AbstractItemsListKeyboard
from src.repository import AbstractRepository


class AbstractItemsListService(ABC):
    repository: Type[AbstractRepository] = None
    keyboard: Type[AbstractItemsListKeyboard] = None


