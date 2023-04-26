"""add few columns to posts table

Revision ID: 0b8ab76631e8
Revises: 93cf20dc2c0e
Create Date: 2023-04-25 14:17:52.521063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b8ab76631e8'
down_revision = '93cf20dc2c0e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(),server_default='True',nullable=False))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('Now()')))
   
    pass
    


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
   
    pass
