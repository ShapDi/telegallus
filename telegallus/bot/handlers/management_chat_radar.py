from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery,Message
from telethon import TelegramClient
from telethon.sessions import StringSession

from telegallus.bot.keyboards.main_menu_kb import keyboard_chat_radars, keyboard_main, keyboards_cancellation
from telegallus.database.schemes import MonitoredChat, AccountTgData
from telegallus.settings import parameters_col

router = Router()

@router.callback_query(F.data.startswith("management_chat_radar"))
async def handle_delete_data(callback_query: CallbackQuery, state: FSMContext):
    chats = await MonitoredChat().get_monitored_chat()
    user_id = callback_query.data.split(".")[1]
    # await callback_query.message.reply(f"{core_client_tg}")
    account = await AccountTgData(user_bot_id=user_id).get_tg_account()
    await callback_query.message.bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
        text="Выбери опцию", reply_markup=keyboard_chat_radars(chats, user_id)
    )

class ChatState(StatesGroup):
    link = State()

@router.callback_query(F.data.startswith("add_tracked_chat"))
async def handle_delete_data(callback_query: CallbackQuery, state: FSMContext):
    chats = await MonitoredChat().get_monitored_chat()
    print(callback_query.data.split("."))
    user_id = callback_query.data.split(".")[1]
    await callback_query.message.bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
        text="Отправь ссылку на чат", reply_markup=keyboards_cancellation()
    )
    await state.update_data(user_id=user_id)
    await state.update_data(update_message=callback_query.message.message_id)
    await state.set_state(ChatState.link)

@router.message(ChatState.link)
async def process_delete_user(message: Message, state: FSMContext):
    await message.delete()
    link = message.text.strip()
    print(link)
    data = await state.get_data()
    from telethon.tl.functions.channels import JoinChannelRequest
    try:
        core_client_tg = await TelegramClient(StringSession(parameters_col.CORE_SESSION_TOKEN),
                                        api_id=int(parameters_col.CORE_API_ID),
                                        api_hash=parameters_col.CORE_API_HASH).start()
        chat = await core_client_tg.get_entity(link)
        print(chat)
        monitored_chat = await MonitoredChat(chat_tg_id=str(chat.id),name=chat.title,user_bot_id=data.get("user_id")).add_monitored_chat()
        print(monitored_chat)
        # await core_client_tg(JoinChannelRequest(chat))
    except Exception as ex:
        print(ex)

    await state.clear()
    await message.bot.edit_message_text(chat_id=message.chat.id, message_id=data.get("update_message"),
        text="Отправьте api_hash для управления ботом", reply_markup=keyboard_main(message.chat.id)
    )




