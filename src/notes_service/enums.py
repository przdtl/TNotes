from src.list_items.enums import BaseItemsCallbackData


class VaultsCallbackData(BaseItemsCallbackData, item_name='vault'):
    pass


class NotesCallbackData(BaseItemsCallbackData, item_name='note'):
    pass
