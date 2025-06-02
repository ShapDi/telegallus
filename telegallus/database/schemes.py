import uuid
from cryptography.fernet import Fernet
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
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.ext.hybrid import hybrid_property


from telegallus.database.engine import get_session_factory
from telegallus.settings import parameters_col


cipher = Fernet(parameters_col.KEY_SEC.encode('utf-8'))
encrypted = cipher.encrypt(b"15426378Dima")

decrypted = cipher.decrypt(encrypted)


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
                return users_tg_id[0].id
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
    api_id: Mapped[str|None] = mapped_column(String, nullable=True, unique=False)
    api_hash: Mapped[str|None] = mapped_column(String, nullable=True, unique=False)
    user_bot_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_bot.id", ondelete="SET NULL"), nullable=True
    )

    @property
    def api_id_account(self) -> str | None:
        if self.api_id is None:
            return None
        decrypt = cipher.decrypt(self.api_id.encode('utf-8'))
        return decrypt.decode('utf-8')

    @api_id_account.setter
    def api_id_account(self, value: str) -> None:
        if value is None:
            self.api_id = None
        else:
            encrypt = cipher.encrypt(value.encode('utf-8'))
            self.api_id = encrypt.decode('utf-8')

    @property
    def api_hash_account(self) -> str| None:
        if self.api_hash is None:
            return None
        decrypt = cipher.decrypt(self.api_hash.encode('utf-8'))
        return decrypt.decode('utf-8')

    @api_hash_account.setter
    def api_hash_account(self, value: str) -> None:
        if value is None:
            self.api_hash = None
        else:
            encrypt = cipher.encrypt(value.encode('utf-8'))
            self.api_hash = encrypt.decode('utf-8')

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

    async def get_tg_account(self):
        async with get_session_factory() as session:
            query = select(AccountTgData).where(or_(AccountTgData.user_bot_id == self.user_bot_id))
            data = await session.execute(query)
            data = data.scalars().all()
            return data

    async def get_tg_account_id(self):
        async with get_session_factory() as session:
            query = select(AccountTgData).where(or_(AccountTgData.id == self.id))
            data = await session.execute(query)
            data = data.scalars().all()
            return data

    async def get_account_tg_data(self, session):
        query = select(AccountTgData).where(or_(AccountTgData.name_account == self.name_account))
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

    @property
    def bot_key_protected(self) -> str | None:
        if self.bot_key is None:
            return None
        decrypt = cipher.decrypt(self.bot_key.encode('utf-8'))
        return decrypt.decode('utf-8')

    @bot_key_protected.setter
    def bot_key_protected(self, value: str) -> None:
        if value is None:
            self.bot_key = None
        else:
            encrypt = cipher.encrypt(value.encode('utf-8'))
            self.bot_key = encrypt.decode('utf-8')

    @property
    def session_id_bot(self) -> str | None:
        if self.session_id is None:
            return None
        decrypt = cipher.decrypt(self.session_id.encode('utf-8'))
        return decrypt.decode('utf-8')

    @session_id_bot.setter
    def session_id_bot(self, value: str) -> None:
        if value is None:
            self.session_id = None
        else:
            encrypt = cipher.encrypt(value.encode('utf-8'))
            self.session_id = encrypt.decode('utf-8')

    async def get_telegram_bot(self, session):
        query = select(TelegramBot).where(or_(TelegramBot.account_tg_pars_id == self.account_tg_pars_id))
        data = await session.execute(query)
        data = data.scalars().all()
        return data

    async def get_account_tg_data(self):
        async with get_session_factory() as session:
            query = select(TelegramBot).where(or_(TelegramBot.account_tg_pars_id == self.account_tg_pars_id))
            data = await session.execute(query)
            data = data.scalars().all()
            return data

    async def add_bots(self):
        async with get_session_factory() as session:
            bots = await self.get_telegram_bot(session)
            if bots:
                return bots
            session.add(self)
            await session.flush()
            id = self.id
            await session.commit()
            return id

class ReplicationChat(Base):
    __tablename__ = "replication_chats"

    chat_tg_id: Mapped[str] = mapped_column(String, nullable=True, unique=False)

class MonitoredChat(Base):
    __tablename__ = "monitored_chats"

    chat_tg_id: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    name: Mapped[str] = mapped_column(String, nullable=True, unique=False)

    async def get_monitored_chat(self):
        async with get_session_factory() as session:
            query = select(MonitoredChat)
            data = await session.execute(query)
            data = data.scalars().all()
            return data

class MessageMonitoredChat(Base):
    __tablename__ = "message_monitored_chat"

    text: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    message_id: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    chat_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("monitored_chats.id", ondelete="SET NULL"), nullable=True
    )

