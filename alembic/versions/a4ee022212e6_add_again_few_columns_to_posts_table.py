"""add again few columns to posts table

Revision ID: a4ee022212e6
Revises: f324a61fd323
Create Date: 2023-04-24 17:57:33.339963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4ee022212e6'
down_revision = 'b339a95efbc4'
branch_labels = None
depends_on = None


def upgrade() -> None:
     op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'),)
     op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
     pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
