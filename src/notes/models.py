import enum
import uuid
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class PointType(enum.Enum):
    FOLDER = 'FOLDER'
    NOTE = 'NOTE'


class Vault(Base):
    __tablename__ = 'vault'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    user_id = Column(ForeignKey('user.id'))

    user = relationship('User', back_populates='vaults')
    points: Mapped['VaultPoint'] = relationship(back_populates='vault')

    def __str__(self):
        return f'{self.user_id}:{self.name}'


class VaultPoint(Base):
    __tablename__ = 'vault_point'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))
    vault_id = Column(ForeignKey('vault.id'))
    parent_id = Column(ForeignKey('vault_point.id'))
    message_id: Mapped[Optional[int]]
    point_type: Mapped[PointType]

    vault: Mapped['Vault'] = relationship(back_populates='points')

    __table_args__ = (
        UniqueConstraint('name', 'vault_id', name='vault_point_name_constraint'),
    )
