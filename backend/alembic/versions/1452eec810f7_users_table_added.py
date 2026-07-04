"""users table added

Revision ID: 1452eec810f7
Revises: 518a1344cd96
Create Date: 2026-07-01 14:54:26.715402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1452eec810f7'
down_revision: Union[str, Sequence[str], None] = '518a1344cd96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=225), nullable=False),
        sa.Column('email', sa.String(length=225), nullable=False),
        sa.Column('hashed_password', sa.String(length=225), nullable=False),
        sa.Column('role', sa.String(length=225), nullable=False, server_default='Candidate'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
