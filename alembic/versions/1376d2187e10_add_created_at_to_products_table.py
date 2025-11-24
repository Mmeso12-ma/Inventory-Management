"""add created_at to products table

Revision ID: 1376d2187e10
Revises: 559247d9576b
Create Date: 2025-11-13 22:37:28.273214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1376d2187e10'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('products', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('products', 'created_at')
    pass
