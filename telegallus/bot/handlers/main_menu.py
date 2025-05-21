from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from telegallus.bot.keyboards.main_menu_kb import keyboard_main

router = Router()

@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer("Выбери пункт меню", reply_markup=keyboard_main())
    print(message)

@router.message(F.text.lower() == '❌ отмена ввода данных')
async def quit(message: Message, state: FSMContext, callback=None):
    await state.clear()
    await message.answer('❌ Ввод отменен', reply_markup=ReplyKeyboardRemove())
    await message.answer('Выбери пункт меню', reply_markup=keyboard_main())

class AccountTg(StatesGroup):
    api_id = State()
    api_hash = State()

class