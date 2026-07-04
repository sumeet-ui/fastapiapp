"""create users table

Revision ID: b83d38f4a7d1
Revises: 1452eec810f7
Create Date: 2026-07-01 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b83d38f4a7d1'
down_revision: Union[str, Sequence[str], None] = '1452eec810f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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
    op.drop_table('users')
