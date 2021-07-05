"""initial revision

Revision ID: 1e3e64c55205
Revises: 
Create Date: 2021-07-04 17:44:02.439458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e3e64c55205'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')


def downgrade():
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
