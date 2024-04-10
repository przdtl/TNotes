from src.notes_service.models import Vault, VaultPoint
from src.repository import SQLAlchemyRepository


class VaultRepository(SQLAlchemyRepository):
    model = Vault


class NoteRepository(SQLAlchemyRepository):
    model = VaultPoint
