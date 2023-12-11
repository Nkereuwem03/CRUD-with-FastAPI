"""add content column to blog table

Revision ID: 2e24e312088b
Revises: 4fd8bf4c81a7
Create Date: 2023-12-06 17:55:49.397792

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e24e312088b'
down_revision: Union[str, None] = '4fd8bf4c81a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('blog', sa.Column("content", sa.String(), nullable=False))

def downgrade() -> None:
    op.drop_column('blog', 'content')
