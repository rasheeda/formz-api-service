"""Add is_webhooks column

Revision ID: 37f5a871b3be
Revises: a99bf4d7876f
Create Date: 2019-10-20 00:32:25.359071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37f5a871b3be'
down_revision = 'a99bf4d7876f'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE form ADD COLUMN is_webhook TINYINT DEFAULT 0;")


def downgrade():
    op.execute("ALTER TABLE form DROP COLUMN is_webhook")
