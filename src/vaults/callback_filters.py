import uuid

from aiogram.filters.callback_data import CallbackData


class VaultsListVaultCallback(CallbackData, prefix='vaults_list_vault'):
    vault_uuid_id: uuid.UUID


class VaultsListPageCallback(CallbackData, prefix='vaults_list_page'):
    page: int
    size: int
    is_next: bool
