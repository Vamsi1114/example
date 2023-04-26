"""add foreign-key to posts table

Revision ID: 93cf20dc2c0e
Revises: 6f517f7e9983
Create Date: 2023-04-25 12:57:39.651282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93cf20dc2c0e'
down_revision = '6f517f7e9983'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table="posts",referent_table="users",local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
