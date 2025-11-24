"""add email column to suppliers table

Revision ID: 8717e99fcc91
Revises: 1376d2187e10
Create Date: 2025-11-13 22:38:34.054806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8717e99fcc91'
down_revision: Union[str, Sequence[str], None] = '1376d2187e10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
