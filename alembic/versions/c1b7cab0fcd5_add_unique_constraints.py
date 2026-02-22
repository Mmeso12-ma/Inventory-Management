"""add_unique_constraints

Revision ID: c1b7cab0fcd5
Revises: 0af32585360e
Create Date: 2026-02-22 23:22:41.439082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1b7cab0fcd5'
down_revision: Union[str, Sequence[str], None] = 'ecb72c2f9118'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint('uq_products_name', 'products', ['name'])
    op.create_unique_constraint('uq_users_username', 'users', ['username'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_products_name', 'products', type_='unique')
    op.drop_constraint('uq_users_username', 'users', type_='unique')
