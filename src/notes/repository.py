from src.notes.models import VaultPoint
from src.repository import SQLAlchemyRepository


class VaultPointRepository(SQLAlchemyRepository):
    model = VaultPoint
