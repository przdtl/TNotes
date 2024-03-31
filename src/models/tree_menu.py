import enum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column
from typing import Optional

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class PointType(enum.Enum):
    FOLDER = 'FOLDER'
    BLOB = 'BLOB'


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    user_id = Column(ForeignKey('user.id'))


class MenuPoint(Base):
    __tablename__ = 'menu_point'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))
    menu_id = Column(ForeignKey('menu.id'))
    parent_id = Column(ForeignKey('menu_point.id'))
    message_id: Mapped[Optional[int]]
    point_type: Mapped[PointType]

    __table_args__ = (
        UniqueConstraint('name', 'menu_id', name='menu_point_name_constraint'),
    )
