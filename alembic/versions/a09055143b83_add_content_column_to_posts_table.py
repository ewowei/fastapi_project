"""add content column to posts table

Revision ID: a09055143b83
Revises: ac73c23def83
Create Date: 2023-08-02 20:05:58.354508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a09055143b83'
down_revision = 'ac73c23def83'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False)) # type: ignore
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
