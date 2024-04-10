from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from src.main_menu.keyboards import main_menu_keyboards
from src.states import BaseStates
from src.user.repository import UserRepository
from src.user.service import UserService

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user = await UserService(UserRepository).get_or_create_user(chat_id=message.chat.id)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!",
                         reply_markup=main_menu_keyboards.main_menu_keyboard())
    await state.set_state(BaseStates.start_state)


# Последний хендлер
@router.message(
    StateFilter(BaseStates.start_state),
)
async def handler_of_everything_handler(message: Message):
    await message.answer(f'Вы находитесь в состоянии start_state')


@router.message()
async def all_messages(message: Message):
    await message.answer(message.text)
