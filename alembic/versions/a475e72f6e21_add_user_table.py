"""ADD User Table

Revision ID: a475e72f6e21
Revises: 07da2dab62b0
Create Date: 2025-06-23 21:45:56.907735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a475e72f6e21'
down_revision: Union[str, Sequence[str], None] = '07da2dab62b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
                    sa.Column('id',sa.Integer(), nullable = False),
                    sa.Column('email',sa.String(),nullable = False , unique=True),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False),
                    sa.PrimaryKeyConstraint('id'))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
