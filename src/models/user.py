import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column
from sqlalchemy.orm import Mapped

from src.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_chat_id: Mapped[int]
    telegram_user_id: Mapped[int]
