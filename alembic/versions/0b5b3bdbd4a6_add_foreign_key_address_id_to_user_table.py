"""add foreign key address id to user table

Revision ID: 0b5b3bdbd4a6
Revises: 1d97dddc5661
Create Date: 2021-07-11 12:15:21.891677

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0b5b3bdbd4a6'
down_revision = '1d97dddc5661'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('address_id', postgresql.UUID(as_uuid=True), nullable=False))
    op.create_foreign_key('fk_address_user', 'users', 'address', ['address_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_address_user', 'users', type_='foreignkey')
    op.drop_column('users', 'address_id')
    # ### end Alembic commands ###
