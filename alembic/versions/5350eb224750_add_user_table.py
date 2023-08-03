"""add user table

Revision ID: 5350eb224750
Revises: a09055143b83
Create Date: 2023-08-02 20:15:05.608655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5350eb224750'
down_revision = 'a09055143b83'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False ),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
                              
    pass


def downgrade():
    op.drop_table('users')
    pass
