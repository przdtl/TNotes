from src.repository import SQLAlchemyRepository
from src.vaults.models import Vault


class VaultRepository(SQLAlchemyRepository):
    model = Vault

