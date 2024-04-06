import uuid

from sqlalchemy import Column
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Vault(Base):
    __tablename__ = 'vault'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User', back_populates='vaults', passive_deletes=True)
    points = relationship('VaultPoint', back_populates='vault', passive_deletes=True)

    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='user_vault_name_constraint'),
    )

    def __str__(self):
        return f'{self.user_id}:{self.name}'
