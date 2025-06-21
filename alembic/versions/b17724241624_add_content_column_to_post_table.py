"""add content column to post table

Revision ID: b17724241624
Revises: 2f2212332a1b
Create Date: 2025-06-21 18:31:35.171887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b17724241624'
down_revision: Union[str, Sequence[str], None] = '2f2212332a1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
