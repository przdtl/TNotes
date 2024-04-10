from src.list_items.callback_filters import ItemsListRightPageClickCallbackFilter, ItemsListLeftPageClickCallbackFilter

from src.list_items.callback_filters import ItemsListItemClickCallbackFilter


# Vaults
class VaultsListVaultClickCallbackFilter(ItemsListItemClickCallbackFilter,
                                         prefix='vaults_list_vault_click'):
    pass


class VaultsListRightPageClickCallbackFilter(ItemsListRightPageClickCallbackFilter,
                                             prefix='vaults_list_right_page_click'):
    pass


class VaultsListLeftPageClickCallbackFilter(ItemsListLeftPageClickCallbackFilter,
                                            prefix='vaults_list_left_page_click'):
    pass


# Notes
class NotesListNoteClickCallbackFilter(ItemsListItemClickCallbackFilter,
                                       prefix='notes_list_note_click'):
    pass


class NotesListRightPageClickCallbackFilter(ItemsListRightPageClickCallbackFilter,
                                            prefix='notes_list_right_page_click'):
    pass


class NotesListLeftPageClickCallbackFilter(ItemsListLeftPageClickCallbackFilter,
                                           prefix='notes_list_left_page_click'):
    pass
