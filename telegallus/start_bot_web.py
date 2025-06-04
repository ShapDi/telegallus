
from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

# from service_connection.back_server_airtable_requests import get_contacts_india


from initialization_bot import bot, dp
from settings import parameters_col

# print(asyncio.run(get_contacts_india("recnfEZVQPz2k1CPg")))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(
        url=f"{parameters_col.BOT_URL}/webhook",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    yield
    await bot.delete_webhook()


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(app, port=2222)
