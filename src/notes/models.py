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
    name: Mapped[str] = mapped_column(String(255))
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User', back_populates='vaults', passive_deletes=True)
    points: Mapped['VaultPoint'] = relationship(back_populates='vault', passive_deletes=True)

    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='user_vault_name_constraint'),
    )

    def __str__(self):
        return f'{self.user_id}:{self.name}'


class VaultPoint(Base):
    __tablename__ = 'vault_point'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))
    vault_id = Column(ForeignKey('vault.id', ondelete='CASCADE'), nullable=False)
    parent_id = Column(ForeignKey('vault_point.id', ondelete='CASCADE'), default=None, nullable=True)
    message_id: Mapped[Optional[int]] = None
    point_type: Mapped[PointType]

    vault: Mapped['Vault'] = relationship(back_populates='points', passive_deletes=True)

    __table_args__ = (
        UniqueConstraint('name', 'vault_id', name='vault_point_name_constraint'),
    )
