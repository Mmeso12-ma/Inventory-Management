"""add product_name to transaction

Revision ID: 0d9b667807c8
Revises: 23b5363994d5
Create Date: 2025-11-24 20:57:43.739826

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d9b667807c8'
down_revision: Union[str, Sequence[str], None] = '23b5363994d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "transaction",
        sa.Column("product_name", sa.String(), nullable=True),
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("transaction", "product_name")
    
