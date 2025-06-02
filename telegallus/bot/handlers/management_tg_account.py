from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from telethon import TelegramClient
from telethon.errors import ApiIdInvalidError

from telegallus.bot.keyboards.main_menu_kb import keyboard_main, keyboards_cancellation, keyboard_management_tg_account
from telegallus.database.schemes import UserBot, AccountTgData

router = Router()

@router.callback_query(F.data.startswith("management_tg_account"))
async def handle_delete_data(callback_query: CallbackQuery, state: FSMContext):
    print(callback_query.data.split("."))
    account_id = callback_query.data.split(".")[1]
    account = await AccountTgData(user_bot_id=account_id).get_tg_account()
    print(account)
    await callback_query.message.bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
        text="Выбери опцию", reply_markup=keyboard_management_tg_account(account)
    )

class AccountTg(StatesGroup):
    name_account_tg = State()
    api_id = State()
    api_hash = State()

@router.callback_query(F.data == "add_tg_account")
async def handle_delete_start(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
        text="Отправьте имя аккаунта для отображения(Оно должно быть уникально)", reply_markup=keyboards_cancellation()
    )
    await state.update_data(update_message=callback_query.message.message_id)
    await state.set_state(AccountTg.name_account_tg)

@router.message(AccountTg.name_account_tg)
async def handle_delete_user(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    name_account_tg =  message.text.strip()
    await message.bot.edit_message_text(chat_id=message.chat.id, message_id=data.get("update_message"),
        text="Отправьте api_id для управления ботом", reply_markup=keyboards_cancellation()
    )
    await state.update_data(name_account_tg=name_account_tg)
    await state.set_state(AccountTg.api_id)



@router.message(AccountTg.api_id)
async def process_delete_user(message: Message, state: FSMContext):
    await message.delete()
    api_id = message.text.strip()
    data = await state.get_data()
    await state.update_data(api_id=api_id)
    await message.bot.edit_message_text(chat_id=message.chat.id, message_id=data.get("update_message"),
        text="Отправьте api_hash для управления ботом", reply_markup=keyboards_cancellation()
    )


    await state.set_state(AccountTg.api_hash)

@router.message(AccountTg.api_hash)
async def process_delete_user(message: Message, state: FSMContext):
    await message.delete()
    api_hash = message.text.strip()
    data = await state.get_data()
    await state.update_data(api_hash=api_hash)

    data = await state.get_data()
    user_bot_id = await UserBot(users_tg_id=str(message.chat.id)).add_chat_tg()
    print(user_bot_id)
    req = await AccountTgData(name_account = data.get("name_account_tg"), api_id_account = str(data.get("api_id")), api_hash_account= str(data.get("api_hash")), user_bot_id=user_bot_id).add_account_tg_data()
    print(data)
    print(req)
    accounts = await AccountTgData(user_bot_id=user_bot_id).get_tg_account()
    await message.bot.edit_message_text(chat_id=message.chat.id, message_id=data.get("update_message"),
        text="Новый аккаунт добавлен", reply_markup=keyboard_management_tg_account(accounts)
    )
    await state.clear()