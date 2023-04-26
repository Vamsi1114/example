"""add_content_column_to_posts_table

Revision ID: c8b14a77a038
Revises: 34b57ef9bb75
Create Date: 2023-04-24 18:41:24.433613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8b14a77a038'
down_revision = '34b57ef9bb75'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('content',sa.String(),nullable=False),
                  )
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
