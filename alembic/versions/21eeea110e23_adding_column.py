"""Adding column 

Revision ID: 21eeea110e23
Revises: c693cd4e7820
Create Date: 2025-06-23 22:09:14.991725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21eeea110e23'
down_revision: Union[str, Sequence[str], None] = 'c693cd4e7820'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('published', sa.Boolean(), nullable=False , server_default=sa.text("true")),)
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable= False ,server_default=sa.text('NOW()')),)
    pass



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','published')
    op.drop_column('posts',"created_at")
    pass
