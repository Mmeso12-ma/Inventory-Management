"""add_email_to_suppliers_nullable_first

Revision ID: 057f82d27828
Revises: 594f68ee36f5
Create Date: 2025-11-04 21:57:48.965080

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '057f82d27828'
down_revision: Union[str, Sequence[str], None] = '594f68ee36f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
