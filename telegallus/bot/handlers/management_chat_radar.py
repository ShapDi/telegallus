from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from telegallus.bot.keyboards.main_menu_kb import keyboard_chat_radars
from telegallus.database.schemes import MonitoredChat, AccountTgData

router = Router()

@router.callback_query(F.data.startswith("management_chat_radar"))
async def handle_delete_data(callback_query: CallbackQuery, state: FSMContext):
    chats = await MonitoredChat().get_monitored_chat()
    account_id = callback_query.data.split(".")[1]
    account = await AccountTgData(user_bot_id=account_id).get_tg_account()
    await callback_query.message.bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
        text="Выбери опцию", reply_markup=keyboard_chat_radars(chats)
    )

@router.callback_query(F.data.startswith("add_tracked_chat"))
async def handle_delete_data(callback_query: CallbackQuery, state: FSMContext):
    chats = await MonitoredChat().get_monitored_chat()
    account_id = callback_query.data.split(".")[1]
    account = await AccountTgData(user_bot_id=account_id).get_tg_account()
    await callback_query.message.bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
        text="Выбери опцию", reply_markup=keyboard_chat_radars(chats)
    )