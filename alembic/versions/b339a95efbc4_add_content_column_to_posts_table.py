"""add content column to posts table

Revision ID: b339a95efbc4
Revises: ec09c7ac7001
Create Date: 2023-04-24 16:06:18.264518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b339a95efbc4'
down_revision = 'ec09c7ac7001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
