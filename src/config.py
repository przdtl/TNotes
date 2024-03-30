from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    BOT_TOKEN: str

    def __init__(self):
        super().__init__()
        self.__dp = Dispatcher()
        self.__bot = Bot(self.BOT_TOKEN, parse_mode=ParseMode.HTML)

    @property
    def get_postgres_dsn(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def dp(self):
        return self.__dp

    @property
    def bot(self):
        return self.__bot

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
