"""initial migration

Revision ID: 559247d9576b
Revises: 
Create Date: 2025-11-13 22:36:46.948659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '559247d9576b'
down_revision: Union[str, Sequence[str], None] = '8717e99fcc91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
