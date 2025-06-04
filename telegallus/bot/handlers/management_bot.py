from telethon import TelegramClient

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from telethon.sessions import StringSession

from telegallus.bot.keyboards.main_menu_kb import (
    keyboards_cancellation,
    keyboard_management_bot,
)
from telegallus.database.schemes import AccountTgData, TelegramBot

router = Router()


@router.callback_query(F.data.startswith("account"))
async def handle_delete_data(callback_query: CallbackQuery, state: FSMContext):
    print(callback_query.data.split("."))
    account_id = callback_query.data.split(".")[1]
    bots = await TelegramBot(account_tg_pars_id=account_id).get_account_tg_data()
    print(bots)
    user_id = await AccountTgData(id=account_id).get_tg_account_id()
    await callback_query.message.bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Выбери опцию",
        reply_markup=keyboard_management_bot(bots, account_id, user_id[0].user_bot_id),
    )


class BotToken(StatesGroup):
    bot_token = State()


@router.callback_query(F.data.startswith("add_bot"))
async def handle_delete_data(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="Отправь token бота",
        reply_markup=keyboards_cancellation(),
    )
    print(callback_query.data.split("."))
    await state.update_data(account_id=callback_query.data.split(".")[1])
    await state.update_data(update_message=callback_query.message.message_id)
    await state.set_state(BotToken.bot_token)


@router.message(BotToken.bot_token)
async def handle_delete_user(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    print(data)
    print(message.text.strip())
    account_id = data.get("account_id")
    accounts = await AccountTgData(id=account_id).get_tg_account_id()
    print(accounts[0].api_id_account)
    bots = await TelegramBot(account_tg_pars_id=account_id).get_account_tg_data()
    try:
        client = await TelegramClient(
            StringSession(),
            api_id=accounts[0].api_id_account,
            api_hash=accounts[0].api_hash_account,
        ).start(bot_token=message.text.strip())
        session_str = client.session.save()
        tg_bot = await TelegramBot(
            bot_key_protected=message.text.strip(),
            session_id_bot=session_str,
            account_tg_pars_id=account_id,
        ).add_bots()
        print(tg_bot)
        me = await client.get_me()
        print(me.stringify())
    except Exception as ex:
        print(ex)
    print(data)
    await state.clear()
    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data.get("update_message"),
        text="Выбери пункт",
        reply_markup=keyboard_management_bot(bots, account_id, accounts[0].user_bot_id),
    )
