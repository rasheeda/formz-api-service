"""user id columns in tables

Revision ID: a99bf4d7876f
Revises: 659aa6f01be8
Create Date: 2019-08-24 23:42:46.496521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a99bf4d7876f'
down_revision = '659aa6f01be8'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE form ADD COLUMN user_id INT NOT NULL;")


def downgrade():
    op.execute("ALTER TABLE form DROP COLUMN user_id")
