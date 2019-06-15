"""Create users table

Revision ID: efe15e0046fb
Revises:
Create Date: 2019-06-15 22:01:16.795135

"""
from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision = 'efe15e0046fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(200), nullable=False),
        sa.Column('password', sa.String(250), nullable=False),
        sa.Column('api_key', sa.String(250)),
        sa.Column('timezone', sa.String(250)),
        sa.Column('created_at', sa.DateTime, nullable=False, default=datetime.datetime.now().time()),
        sa.Column('updated_at', sa.DateTime, nullable=False, default=datetime.datetime.now().time()),
    )

def downgrade():
    op.drop_table('users')
