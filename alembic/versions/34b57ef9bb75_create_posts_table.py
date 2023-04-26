"""create posts table

Revision ID: 34b57ef9bb75
Revises: 
Create Date: 2023-04-24 16:43:07.226872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34b57ef9bb75'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False))


def downgrade():
    op.drop_table('posts')
    pass
