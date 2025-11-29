"""merge heads

Revision ID: 846c2871d2f1
Revises: 4d07bd3ae63b, c8267f598c7b
Create Date: 2025-11-29 19:00:04.496927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '846c2871d2f1'
down_revision: Union[str, Sequence[str], None] = ('4d07bd3ae63b', 'c8267f598c7b')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
