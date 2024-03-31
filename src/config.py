import asyncpg.connection
import redis
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # DATABASE CONNECTION
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # BOT VARIABLES
    BOT_TOKEN: str

    # CACHE CONNECTION
    CACHE_NAME: str
    CACHE_PASS: str
    CACHE_HOST: str
    CACHE_PORT: str

    def __init__(self):
        super().__init__()
        self.__init_storage()
        self.__dp = Dispatcher(storage=self.__storage)
        self.__bot = Bot(self.BOT_TOKEN, parse_mode=ParseMode.HTML)

    def __init_storage(self):
        r = self.get_redis
        try:
            r.ping()
            self.__storage = RedisStorage(self.get_redis)
        except (redis.exceptions.ConnectionError, ConnectionRefusedError):
            self.__storage = MemoryStorage()

    @property
    def get_postgres_dsn(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def get_redis(self):
        return redis.Redis(host=self.CACHE_HOST, port=self.CACHE_PORT, db=self.CACHE_NAME, password=self.CACHE_PASS)

    @property
    def dp(self):
        return self.__dp

    @property
    def bot(self):
        return self.__bot

    @property
    def storage(self):
        return self.__storage

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
