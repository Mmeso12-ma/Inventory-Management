"""merge heads

Revision ID: 4d07bd3ae63b
Revises: ffdeabc8e86a, 0d9b667807c8
Create Date: 2025-11-24 21:37:56.745397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d07bd3ae63b'
down_revision: Union[str, Sequence[str], None] = ('ffdeabc8e86a', '0d9b667807c8')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
