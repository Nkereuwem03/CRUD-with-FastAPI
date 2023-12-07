"""add last few columns to blog table

Revision ID: fe16ce3163d3
Revises: f8aacb81976a
Create Date: 2023-12-06 20:20:50.759065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe16ce3163d3'
down_revision: Union[str, None] = 'f8aacb81976a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('blog', sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False)),
    op.add_column('blog', sa.Column('date_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('blog', 'published')
    op.drop_column('blog', 'date_created')
    pass
