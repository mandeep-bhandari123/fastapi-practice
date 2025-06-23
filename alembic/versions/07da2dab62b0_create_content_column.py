"""Create content column

Revision ID: 07da2dab62b0
Revises: 2f2212332a1b
Create Date: 2025-06-21 18:35:45.071640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07da2dab62b0'
down_revision: Union[str, Sequence[str], None] = '2f2212332a1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass