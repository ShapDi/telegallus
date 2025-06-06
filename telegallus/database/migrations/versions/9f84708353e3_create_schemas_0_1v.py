"""create schemas 0.1v

Revision ID: 9f84708353e3
Revises:
Create Date: 2025-05-24 22:06:29.306469

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9f84708353e3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "monitored_chats",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("chat_tg_id", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "replication_chats",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("chat_tg_id", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_bot",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("users_tg_id", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "accounts_tg_pars",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("api_id", sa.String(), nullable=True),
        sa.Column("api_hash", sa.String(), nullable=True),
        sa.Column("session_id", sa.String(), nullable=True),
        sa.Column("user_bot_id", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(["user_bot_id"], ["user_bot.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "message_monitored_chat",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("text", sa.String(), nullable=True),
        sa.Column("message_id", sa.String(), nullable=True),
        sa.Column("chat_id", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(
            ["chat_id"], ["monitored_chats.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "telegram_bots",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("bot_key", sa.String(), nullable=True),
        sa.Column("account_tg_pars_id", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(
            ["account_tg_pars_id"], ["accounts_tg_pars.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("telegram_bots")
    op.drop_table("message_monitored_chat")
    op.drop_table("accounts_tg_pars")
    op.drop_table("user_bot")
    op.drop_table("replication_chats")
    op.drop_table("monitored_chats")
    # ### end Alembic commands ###
