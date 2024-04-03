from src.user.models import User
from src.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
