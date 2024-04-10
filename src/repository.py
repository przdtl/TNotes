from abc import ABC, abstractmethod
from sqlalchemy import select, insert
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from src.database import async_session_maker


class AbstractRepository(ABC):
    model = None

    @classmethod
    @abstractmethod
    async def get(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_all(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_related_objects(cls, object_id, name_of_relative):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_count(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def insert(cls, **data):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def update(cls, pk, **data):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def delete(cls, pk):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    @classmethod
    async def get(cls, **kwargs):
        result = await cls.get_all(**kwargs)
        if not result:
            raise NoResultFound
        if len(result) > 1:
            raise MultipleResultsFound
        return result[0]

    @classmethod
    async def get_all(cls, **kwargs):
        async with async_session_maker() as session:
            result = await session.scalars(select(cls.model).filter_by(**kwargs).order_by(cls.model.id))
            return result.all()

    @classmethod
    async def get_related_objects(cls, object_id, name_of_relative):
        async with async_session_maker() as session:
            model_item = await session.get(cls.model, object_id)
            items = await getattr(getattr(model_item, 'awaitable_attrs'), name_of_relative)
            return items

    @classmethod
    async def get_count(cls, **kwargs):
        async with async_session_maker() as session:
            return len((await session.scalars(select(cls.model).filter_by(**kwargs))).all())

    @classmethod
    async def insert(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    @classmethod
    async def update(cls, pk, **data):
        async with async_session_maker() as session:
            stmt = await session.get(cls.model, pk)

            if not stmt:
                raise NoResultFound

            for key, value in data.items():
                setattr(stmt, key, value)
            await session.commit()
            return stmt

    @classmethod
    async def delete(cls, pk):
        async with async_session_maker() as session:
            stmt = await session.get(cls.model, pk)

            if not stmt:
                raise NoResultFound

            await session.delete(stmt)
            await session.commit()
