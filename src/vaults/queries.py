from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.base.keyboards import base_keyboards
from src.vaults.callback_filters import VaultsListVaultCallback, VaultsListPageCallback
from src.vaults.enums import VaultsCallbackHandlers
from src.vaults.repository import VaultRepository
from src.vaults.service import VaultService
from src.states import BaseStates, VaultsStates

router = Router()


# Выводит список томов
@router.callback_query(
    F.data == VaultsCallbackHandlers.VAULTS_LIST,
    StateFilter(BaseStates.start_state),
)
async def view_vaults_list_callback_query(callback_query: CallbackQuery, state: FSMContext):
    await VaultService(VaultRepository).list_vaults(callback_query.message, state)


# Возврат на главную страницу с списка томов
@router.callback_query(
    F.data == VaultsCallbackHandlers.GO_HOME_FROM_VAULTS_LIST,
    StateFilter(VaultsStates.list_vaults),
)
async def go_home_from_vaults_list_callback_query(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(BaseStates.start_state)
    await callback_query.message.edit_text(text='Вы вернулись на главное меню',
                                           reply_markup=base_keyboards.main_menu_keyboard())
    await callback_query.answer()


# Создание нового тома
@router.callback_query(
    F.data == VaultsCallbackHandlers.CREATE_NEW_VAULT,
    StateFilter(VaultsStates.list_vaults),
)
async def create_new_vault_callback_query(callback_query: CallbackQuery,
                                          state: FSMContext):
    await state.set_state(VaultsStates.create_vault)
    await callback_query.message.edit_text(text='Введите название нового хранилища',
                                           reply_markup=base_keyboards.back_keyboard(
                                               VaultsCallbackHandlers.GO_BACK_FROM_CREATE_VAULT))
    await callback_query.answer()


# Удаление тома
@router.callback_query(
    F.data == VaultsCallbackHandlers.DELETE_VAULT,
    StateFilter(VaultsStates.list_vaults),
)
async def delete_vault_callback_query(callback_query: CallbackQuery,
                                      state: FSMContext):
    await state.set_state(VaultsStates.delete_vault)
    await callback_query.message.edit_text(text='Введите название хранилища, которое желаете удалить',
                                           reply_markup=base_keyboards.back_keyboard(
                                               VaultsCallbackHandlers.GO_BACK_FROM_DELETE_VAULT))
    await callback_query.answer()


# Возврат назад с удаления или создания нового тома
@router.callback_query(
    F.data == VaultsCallbackHandlers.GO_BACK_FROM_CREATE_VAULT or F.data == VaultsCallbackHandlers.GO_BACK_FROM_DELETE_VAULT,
    StateFilter(VaultsStates.create_vault, VaultsStates.delete_vault),
)
async def go_back_from_create_vault_callback_query(callback_query: CallbackQuery, state: FSMContext):
    await VaultService(VaultRepository).list_vaults(callback_query.message, state)
    await callback_query.answer()


# Переход по страницам в списке томов
@router.callback_query(
    VaultsListPageCallback.filter(),
    StateFilter(VaultsStates.list_vaults),
)
async def vaults_list_go_to_specific_page_callback_query(
        callback_query: CallbackQuery,
        callback_data: VaultsListPageCallback,
        state: FSMContext,
):
    page = callback_data.page
    size = callback_data.size
    if callback_data.is_next:
        total_count = await VaultService(VaultRepository).get_rows_count()
        if ((page + 1) * size) - size >= total_count:
            await callback_query.answer(text='Вы уже находитесь на последней странице!')
            return
        new_page_number = page + 1

    else:
        if page == 1:
            await callback_query.answer(text='Вы уже находитесь на первой странице!')
            return
        new_page_number = page - 1

    await VaultService(VaultRepository).list_vaults(callback_query.message, state,
                                                    page_number=new_page_number,
                                                    page_size=size)


# Обработчик нажатия на определённый том в списке томов
@router.callback_query(
    VaultsListVaultCallback.filter(),
    StateFilter(VaultsStates.list_vaults),
)
async def vaults_list_vault_callback_query(
        callback_query: CallbackQuery,
        callback_data: VaultsListVaultCallback, ):
    await callback_query.answer(f'{callback_data.vault_uuid_id=}\n'
                                f'{callback_query.data=}', show_alert=True)
