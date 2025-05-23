from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column,
    relationship,
    joinedload,
)
from sqlalchemy import String, ForeignKey
from sqlalchemy import select
import uuid

from engine import get_session_factory



class Base(DeclarativeBase):
    pass

class UserBot(Base):
    __tablename__ = "user_bot"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    user_name: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    users_tg_id: Mapped[str] = mapped_column(String, nullable=True, unique=False)

class AccountTgData(Base):
    __tablename__ = "accounts_tg_pars"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    api_id: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    api_hash: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    session_id: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    user_bot_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_bot.id", ondelete="SET NULL"), nullable=True
    )

class TelegramBot(Base):
    __tablename__ = "telegram_bots"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    bot_key: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    account_tg_pars_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("accounts_tg_pars.id", ondelete="SET NULL"), nullable=True
    )

class ReplicationChat(Base):
    __tablename__ = "replication_chats"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    chat_tg_id: Mapped[str] = mapped_column(String, nullable=True, unique=False)

class MonitoredChat(Base):
    __tablename__ = "monitored_chats"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    chat_tg_id: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    name: Mapped[str] = mapped_column(String, nullable=True, unique=False)

class MessageMonitoredChat(Base):
    __tablename__ = "message_monitored_chat"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    message_id: Mapped[str] = mapped_column(String, nullable=True, unique=False)
    chat_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("monitored_chats.id", ondelete="SET NULL"), nullable=True
    )

