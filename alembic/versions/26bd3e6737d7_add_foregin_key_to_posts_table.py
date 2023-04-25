"""add foregin key to posts table

Revision ID: 26bd3e6737d7
Revises: dcb39689fdbe
Create Date: 2023-04-24 16:33:49.850492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26bd3e6737d7'
down_revision = 'dcb39689fdbe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table="posts",referent_table="users",local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
