from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.handlers.main_menu import router as main_router
from settings import get_parameters, parameters_col


bot = Bot(
    token=parameters_col.BOT_CODE,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()
dp.include_routers(main_router)