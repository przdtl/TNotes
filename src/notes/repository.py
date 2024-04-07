from src.notes.models import VaultPoint
from src.repository import SQLAlchemyRepository


class NoteRepository(SQLAlchemyRepository):
    model = VaultPoint
