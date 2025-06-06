"""create schemas 0.6v

Revision ID: 1afdedb09062
Revises: 6ae43e7df425
Create Date: 2025-05-26 14:16:45.017491

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1afdedb09062"
down_revision: Union[str, None] = "6ae43e7df425"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("accounts_tg_pars", sa.Column("api_id", sa.String(), nullable=True))
    op.drop_column("accounts_tg_pars", "_api_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "accounts_tg_pars",
        sa.Column("_api_id", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_column("accounts_tg_pars", "api_id")
    # ### end Alembic commands ###
