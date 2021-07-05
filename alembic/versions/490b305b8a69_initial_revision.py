"""initial revision

Revision ID: 490b305b8a69
Revises: 
Create Date: 2021-07-05 16:31:52.001696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '490b305b8a69'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')


def downgrade():
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
