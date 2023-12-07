"""added users table

Revision ID: f55bd715a07d
Revises: 2e24e312088b
Create Date: 2023-12-06 18:21:09.298139

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f55bd715a07d'
down_revision: Union[str, None] = '2e24e312088b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), index=True, primary_key=True, nullable=False, unique=True),
                    sa.Column('username', sa.String(), unique=True, index=True, nullable=False),
                    sa.Column('email', sa.String(), unique=True, index=True, nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('is_active', sa.Boolean(), default=True))
    pass
                    


def downgrade() -> None:
    op.drop_table('users')
    pass
