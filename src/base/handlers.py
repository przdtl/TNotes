from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from src.base.keyboards import base_keyboards
from src.states import BaseStates
from src.user.repository import UserRepository
from src.user.service import UserService

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user = await UserService(UserRepository).get_or_create_user(chat_id=message.chat.id)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!",
                         reply_markup=base_keyboards.main_menu_keyboard())
    await state.set_state(BaseStates.start_state)


@router.message(
    Command('go'),
    StateFilter(BaseStates.start_state),
)
async def fffffff(message: Message, state: FSMContext):
    await message.answer('start state')


@router.message(
    Command('back'),
    StateFilter(BaseStates.start_state),
)
async def back(message: Message, state: FSMContext):
    await message.answer('state is back')
    await state.set_state(None)


@router.message(Command('go'))
async def command_go_handler(mesaage: Message) -> None:
    await mesaage.answer('hello go')


@router.message()
async def all_messages(message: Message):
    await message.answer(message.text)
