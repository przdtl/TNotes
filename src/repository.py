from abc import ABC, abstractmethod
from sqlalchemy import select, insert, func
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from src.database import async_session_maker


class AbstractRepository(ABC):
    model = None

    @abstractmethod
    async def get(self, **kwargs):
        raise NotImplementedError

    async def get_all(self, **kwargs):
        raise NotImplementedError

    async def get_related_objects(self, object_id, name_of_relative):
        raise NotImplementedError

    async def get_count(self, **kwargs):
        raise NotImplementedError

    async def insert(self, **data):
        raise NotImplementedError

    async def update(self, pk, **data):
        raise NotImplementedError

    async def delete(self, pk):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):

    async def get(self, **kwargs):
        result = await self.get_all(**kwargs)
        result = result.all()
        if not result:
            raise NoResultFound
        if len(result) > 1:
            raise MultipleResultsFound
        return result[0]

    async def get_all(self, **kwargs):
        async with async_session_maker() as session:
            result = await session.scalars(select(self.model).filter_by(**kwargs).order_by(self.model.id))
            return result

    async def get_related_objects(self, object_id, name_of_relative):
        async with async_session_maker() as session:
            model_item = await session.get(self.model, object_id)
            items = await getattr(getattr(model_item, 'awaitable_attrs'), name_of_relative)
            return items

    async def get_count(self, **kwargs):
        async with async_session_maker() as session:
            return len((await session.scalars(select(self.model).filter_by(**kwargs))).all())

    async def insert(self, **data):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def update(self, pk, **data):
        async with async_session_maker() as session:
            stmt = await session.get(self.model, pk)

            if not stmt:
                raise NoResultFound

            for key, value in data.items():
                setattr(stmt, key, value)
            await session.commit()
            return stmt

    async def delete(self, pk):
        async with async_session_maker() as session:
            stmt = await session.get(self.model, pk)

            if not stmt:
                raise NoResultFound

            await session.delete(stmt)
            await session.commit()
