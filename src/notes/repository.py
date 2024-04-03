from src.repository import SQLAlchemyRepository
from src.notes.models import (Vault, VaultPoint)


class VaultRepository(SQLAlchemyRepository):
    model = Vault


class VaultPointRepository(SQLAlchemyRepository):
    model = VaultPoint
