import uuid

from aiogram.filters.callback_data import CallbackData


class ItemsListItemClickCallbackFilter(CallbackData, prefix=''):
    item_uuid_id: uuid.UUID


class ItemsListPageClickCallbackFilter(CallbackData, prefix=''):
    page: int
    size: int


class ItemsListRightPageClickCallbackFilter(ItemsListPageClickCallbackFilter, prefix=''):
    pass


class ItemsListLeftPageClickCallbackFilter(ItemsListPageClickCallbackFilter, prefix=''):
    pass
