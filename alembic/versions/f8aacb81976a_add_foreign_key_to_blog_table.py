"""add foreign-key to blog table

Revision ID: f8aacb81976a
Revises: f55bd715a07d
Create Date: 2023-12-06 19:29:27.474924

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8aacb81976a'
down_revision: Union[str, None] = 'f55bd715a07d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('blog', sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("blog_users_fk", source_table='blog', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('blog_users_fk', table_name='blog')
    op.drop_column('blog', 'owner_id')
    pass
