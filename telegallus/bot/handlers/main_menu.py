from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from telegallus.bot.keyboards.main_menu_kb import keyboard_main
from telegallus.database.schemes import UserBot

router = Router()

@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.delete()

    data = await UserBot(username=message.chat.username, last_name=message.chat.last_name, first_name=message.chat.first_name, users_tg_id=str(message.chat.id)).add_chat_tg()
    print(data)

    await message.bot.send_message(chat_id=message.chat.id,
                                             text="Выбери пункт меню",
                                             reply_markup=keyboard_main())


@router.callback_query(F.data == "keyboard_remover")
async def quit(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
        text="Выбери пункт меню", reply_markup=keyboard_main()
    )

