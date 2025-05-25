from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column,
    relationship,
    joinedload,
)
from sqlalchemy import String, ForeignKey
from sqlalchemy import select
from sqlalchemy.sql import or_
import uuid

from telegallus.database.engine import get_session_factory


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)

    async def create_record(self, session):
        session.add(self)
        await session.flush()
        id = self.id
        await session.commit()
        return id

class UserBot(Base):
    __tablename__ = "user_bot"

    username: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    last_name: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    first_name: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    users_tg_id: Mapped[str] = mapped_column(String, nullable=True, unique=False)


    async def add_chat_tg(self):
        async with get_session_factory() as session:
            users_tg_id = await self.get_users_tg_id(self.users_tg_id, session)
            if users_tg_id:
                return users_tg_id
            session.add(self)
            await session.flush()
            id = self.id
            await session.commit()
            return id

    @staticmethod
    async def get_users_tg_id(users_tg_id, session):
        query = select(UserBot).where(UserBot.users_tg_id == users_tg_id)
        data = await session.execute(query)
        data = data.scalars().all()
        return data

class AccountTgData(Base):
    __tablename__ = "accounts_tg_pars"


    name_account: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    api_id: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    api_hash: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    user_bot_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_bot.id", ondelete="SET NULL"), nullable=True
    )


    async def add_account_tg_data(self):
        async with get_session_factory() as session:
            users_tg_id = await self.get_account_tg_data(session)
            if users_tg_id:
                return users_tg_id
            session.add(self)
            await session.flush()
            id = self.id
            await session.commit()
            return id

    async def get_account_tg_data(self, session):
        query = select(AccountTgData).where(or_(AccountTgData.name_account == self.name_account, AccountTgData.api_id == self.api_id))
        print(query)
        data = await session.execute(query)
        data = data.scalars().all()
        return data



class TelegramBot(Base):
    __tablename__ = "telegram_bots"


    bot_key: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    session_id: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    account_tg_pars_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("accounts_tg_pars.id", ondelete="SET NULL"), nullable=True
    )

class ReplicationChat(Base):
    __tablename__ = "replication_chats"

    chat_tg_id: Mapped[str] = mapped_column(String, nullable=True, unique=False)

class MonitoredChat(Base):
    __tablename__ = "monitored_chats"

    chat_tg_id: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    name: Mapped[str] = mapped_column(String, nullable=True, unique=False)

class MessageMonitoredChat(Base):
    __tablename__ = "message_monitored_chat"

    text: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    message_id: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    chat_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("monitored_chats.id", ondelete="SET NULL"), nullable=True
    )

