import uuid
from aiogram.filters.callback_data import CallbackData


class VaultsListVaultCallback(CallbackData, prefix='vaults_list_vault'):
    vault_uuid_id: uuid.UUID
