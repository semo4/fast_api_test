"""initial revision

Revision ID: c5443fb315b6
Revises: 
Create Date: 2021-07-11 12:12:12.332174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5443fb315b6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')


def downgrade():
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
