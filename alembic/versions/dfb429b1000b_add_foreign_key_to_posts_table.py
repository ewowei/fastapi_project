"""add foreign-key to posts table

Revision ID: dfb429b1000b
Revises: 5350eb224750
Create Date: 2023-08-03 13:37:31.071170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfb429b1000b'
down_revision = '5350eb224750'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(),
                                      nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'],
                          ondelete="CASCADE")
    pass

def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
