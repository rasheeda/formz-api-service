"""Create a tokens blacklist table

Revision ID: 659aa6f01be8
Revises: efe15e0046fb
Create Date: 2019-08-23 23:33:43.026394

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = '659aa6f01be8'
down_revision = 'efe15e0046fb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'revoked_tokens',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('token', sa.String(200), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, default=datetime.datetime.now().time()),
        sa.Column('updated_at', sa.DateTime, nullable=True,
    )

def downgrade():
    op.drop_table('revoked_tokens')
