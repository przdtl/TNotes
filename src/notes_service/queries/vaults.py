from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.base.keyboards import base_keyboards
from src.notes_service.services import VaultsListService
from src.states import BaseStates

router = Router()


# Выводит список томов
@router.callback_query(
    F.data == VaultsListService.keyboard.base_items_callback_data.LIST_OF_ITEMS,
    StateFilter(BaseStates.start_state),
)
async def view_vaults_list_callback_query(callback_query: CallbackQuery, state: FSMContext):
    await VaultsListService.list_items(callback_query.message, state)


# Возврат на главную страницу с списка томов
@router.callback_query(
    F.data == VaultsListService.keyboard.base_items_callback_data.GO_HOME_FROM_LIST_OF_ITEMS,
    StateFilter(VaultsListService.list_items_states_group.list_items),
)
async def go_home_from_vaults_list_callback_query(callback_query: CallbackQuery, state: FSMContext):
    await VaultsListService.go_home_from_items_list(callback_query, state)


# Создание нового тома
@router.callback_query(
    F.data == VaultsListService.keyboard.base_items_callback_data.CREATE_NEW_ITEM,
    StateFilter(VaultsListService.list_items_states_group.list_items),
)
async def create_new_vault_callback_query(callback_query: CallbackQuery,
                                          state: FSMContext):
    await state.set_state(VaultsListService.list_items_states_group.create_item)
    await callback_query.message.edit_text(text='Введите название нового хранилища',
                                           reply_markup=base_keyboards.back_keyboard(
                                               VaultsListService.keyboard.base_items_callback_data.GO_BACK_FROM_CREATE_ITEM))
    await callback_query.answer()


# Удаление тома
@router.callback_query(
    F.data == VaultsListService.keyboard.base_items_callback_data.DELETE_ITEM,
    StateFilter(VaultsListService.list_items_states_group.list_items),
)
async def delete_vault_callback_query(callback_query: CallbackQuery,
                                      state: FSMContext):
    await state.set_state(VaultsListService.list_items_states_group.delete_item)
    await callback_query.message.edit_text(text='Введите название хранилища, которое желаете удалить',
                                           reply_markup=base_keyboards.back_keyboard(
                                               VaultsListService.keyboard.base_items_callback_data.GO_BACK_FROM_DELETE_ITEM))
    await callback_query.answer()


# Возврат назад с удаления или создания нового тома
@router.callback_query(
    F.data == VaultsListService.keyboard.base_items_callback_data.GO_BACK_FROM_CREATE_ITEM or
    F.data == VaultsListService.keyboard.base_items_callback_data.GO_BACK_FROM_DELETE_ITEM,
    StateFilter(VaultsListService.list_items_states_group.create_item,
                VaultsListService.list_items_states_group.delete_item),
)
async def go_back_from_create_vault_callback_query(callback_query: CallbackQuery, state: FSMContext):
    await VaultsListService.list_items(callback_query.message, state)
    await callback_query.answer()


# Переход по страницам в списке томов
@router.callback_query(
    VaultsListService.keyboard.items_list_right_page_click_callback_filter.filter(),
    StateFilter(VaultsListService.list_items_states_group.list_items),
)
async def vaults_list_go_to_specific_page_callback_query(
        callback_query: CallbackQuery,
        callback_data: VaultsListService.keyboard.items_list_right_page_click_callback_filter,
        state: FSMContext,
):
    page = callback_data.page
    size = callback_data.size
    total_count = await VaultsListService.get_rows_count()
    if ((page + 1) * size) - size >= total_count:
        await callback_query.answer(text='Вы уже находитесь на последней странице!')
    else:
        await VaultsListService.list_items(callback_query.message, state,
                                           page_number=page + 1,
                                           page_size=size)


# Переход по страницам в списке томов
@router.callback_query(
    VaultsListService.keyboard.items_list_left_page_click_callback_filter.filter(),
    StateFilter(VaultsListService.list_items_states_group.list_items),
)
async def vaults_list_go_to_left_page_callback_query(
        callback_query: CallbackQuery,
        callback_data: VaultsListService.keyboard.items_list_left_page_click_callback_filter,
        state: FSMContext,
):
    page = callback_data.page
    size = callback_data.size
    if page == 1:
        await callback_query.answer(text='Вы уже находитесь на первой странице!')
    else:
        await VaultsListService.list_items(callback_query.message, state,
                                           page_number=page - 1,
                                           page_size=size)


# Обработчик нажатия на определённый том в списке томов
@router.callback_query(
    VaultsListService.keyboard.items_list_item_click_callback_filter.filter(),
    StateFilter(VaultsListService.list_items_states_group.list_items),
)
async def vaults_list_vault_callback_query(
        callback_query: CallbackQuery,
        callback_data: VaultsListService.keyboard.items_list_item_click_callback_filter, ):
    await callback_query.answer(f'{callback_data.item_uuid_id=}\n'
                                f'{callback_query.data=}', show_alert=True)
