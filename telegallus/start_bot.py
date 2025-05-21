import asyncio
from telegallus.initialization_bot import bot, dp


async def start():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("start bot")
    asyncio.run(start())