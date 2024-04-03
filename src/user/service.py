from typing import Type, Optional

from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from src.database import async_session_maker
from src.repository import AbstractRepository
from src.user.models import User


class UserService:

    def __init__(self, user_repo: Type[AbstractRepository]):
        self.user_repo = user_repo()

    async def get_or_create_user(self, chat_id: int, user_id: Optional[int] = None) -> User:
        try:
            kwargs = {key: value
                      for key, value in {'telegram_chat_id': chat_id, 'telegram_user_id': user_id}.items() if
                      value is not None
                      }
            user: User = await self.user_repo.get(**kwargs)
        except NoResultFound:
            user: User = User(telegram_chat_id=chat_id, telegram_user_id=user_id)
            async with async_session_maker() as session:
                session.add(user)
                await session.commit()
        # except MultipleResultsFound:
        #     pass
        return user
