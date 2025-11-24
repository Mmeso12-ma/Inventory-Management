"""placeholder for missing revision ffdeabc8e86a"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "ffdeabc8e86a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # no-op placeholder to satisfy Alembic revision map
    pass

def downgrade() -> None:
    pass