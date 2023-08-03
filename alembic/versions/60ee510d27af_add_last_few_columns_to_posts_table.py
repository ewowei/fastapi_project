"""add last few columns to posts table

Revision ID: 60ee510d27af
Revises: dfb429b1000b
Create Date: 2023-08-03 16:13:02.906235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60ee510d27af'
down_revision = 'dfb429b1000b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False,
                    server_default="TRUE" ))
    op.add_column('posts',  sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                      nullable=False, server_default=sa.text('now()')))
    pass

def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
