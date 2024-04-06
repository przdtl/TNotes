import enum
import uuid
from typing import Optional

from sqlalchemy import Column, UUID, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base


class PointType(enum.Enum):
    FOLDER = 'FOLDER'
    NOTE = 'NOTE'


class VaultPoint(Base):
    __tablename__ = 'vault_point'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))
    vault_id = Column(ForeignKey('vault.id', ondelete='CASCADE'), nullable=False)
    parent_id = Column(ForeignKey('vault_point.id', ondelete='CASCADE'), default=None, nullable=True)
    message_id: Mapped[Optional[int]] = None
    point_type: Mapped[PointType]

    vault = relationship('Vault', back_populates='points', passive_deletes=True)

    __table_args__ = (
        UniqueConstraint('name', 'vault_id', name='vault_point_name_constraint'),
    )
