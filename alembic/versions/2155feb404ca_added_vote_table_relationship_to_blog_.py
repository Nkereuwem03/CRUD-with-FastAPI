"""added vote-table-relationship to blog table

Revision ID: 2155feb404ca
Revises: 0978cbd0a64b
Create Date: 2023-12-11 11:37:17.927893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2155feb404ca'
down_revision: Union[str, None] = '0978cbd0a64b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('blog', sa.)
    pass


def downgrade() -> None:
    pass
