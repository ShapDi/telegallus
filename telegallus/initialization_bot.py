from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from settings import parameters_col

from bot.handlers.main_menu import router as main_router
from bot.handlers.management_tg_account import router as add_account_tg_router
from bot.handlers.management_bot import router as management_bot_router

bot = Bot(
    token=parameters_col.BOT_CODE,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()
dp.include_routers(main_router)
dp.include_routers(add_account_tg_router)
dp.include_routers(management_bot_router)