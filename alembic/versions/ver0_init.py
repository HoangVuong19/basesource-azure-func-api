"""
init

Revision ID: ver0
Revises:
Create Date: 2025-05-21
"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "ver0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
