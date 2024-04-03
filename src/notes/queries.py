from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.base.keyboards import base_keyboards
from src.notes.callback_filters import VaultsListVaultCallback
from src.notes.enums import NoteCallbackHandlers
from src.notes.repository import VaultRepository
from src.notes.service import VaultService
from src.states import BaseStates, NoteStates

router = Router()


# Возврат на главную страницу с списка томов
@router.callback_query(
    F.data == NoteCallbackHandlers.GO_HOME_FROM_VAULTS_LIST,
    StateFilter(NoteStates.list_vaults),
)
async def go_home_from_vaults_list_callback_query(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(BaseStates.start_state)
    await callback_query.message.answer(text='Вы вернулись на главное меню',
                                        reply_markup=base_keyboards.main_menu_keyboard())
    await callback_query.answer()


# Создание нового тома
@router.callback_query(
    F.data == NoteCallbackHandlers.CREATE_NEW_VAULT,
    StateFilter(NoteStates.list_vaults),
)
async def create_new_vault_callback_query(callback_query: CallbackQuery,
                                          state: FSMContext):
    await state.set_state(NoteStates.create_vault)
    await callback_query.message.edit_text(text='Введите название нового хранилища',
                                           reply_markup=base_keyboards.back_keyboard(
                                               NoteCallbackHandlers.GO_BACK_FROM_CREATE_VAULT))
    await callback_query.answer()


# Удаление тома
@router.callback_query(
    F.data == NoteCallbackHandlers.DELETE_VAULT,
    StateFilter(NoteStates.list_vaults),
)
async def delete_vault_callback_query(callback_query: CallbackQuery,
                                      state: FSMContext):
    await state.set_state(NoteStates.delete_vault)
    await callback_query.message.edit_text(text='Введите название хранилища, которое желаете удалить',
                                           reply_markup=base_keyboards.back_keyboard(
                                               NoteCallbackHandlers.GO_BACK_FROM_DELETE_VAULT))
    await callback_query.answer()


# Возврат назад с удаления или создания нового тома
@router.callback_query(
    F.data == NoteCallbackHandlers.GO_BACK_FROM_CREATE_VAULT or F.data == NoteCallbackHandlers.GO_BACK_FROM_DELETE_VAULT,
    StateFilter(NoteStates.create_vault, NoteStates.delete_vault),
)
async def go_back_from_create_vault_callback_query(callback_query: CallbackQuery, state: FSMContext):
    await VaultService(VaultRepository).list_vaults(callback_query.message, state, is_wo_user_id=True)
    await callback_query.answer()


# Обработчик нажатия на определённый том в списке томов
@router.callback_query(
    VaultsListVaultCallback.filter(),
    StateFilter(NoteStates.list_vaults),
)
async def vaults_list_vault_callback_query(callback_query: CallbackQuery,
                                           callback_data: VaultsListVaultCallback,
                                           state: FSMContext):
    await callback_query.answer(f'{callback_data.vault_uuid_id=}\n'
                                f'{callback_query.data=}', show_alert=True)
