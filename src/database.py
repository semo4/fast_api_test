from datetime import datetime

from decouple import config
from sqlalchemy import (
    Column, DateTime, ForeignKey, Integer, MetaData, String, Table, UniqueConstraint, create_engine,
    func, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.elements import literal_column

DB_URL = config('DB_URL')

engine = create_engine(DB_URL)
metadata = MetaData(bind=engine)

new_uuid = text('uuid_generate_v4()')
now = datetime.utcnow

default_now = dict(default=now, server_default=func.now())

ALL_COLUMNS = literal_column('*')

users = Table(
    'users', metadata,
    Column('id',
           UUID(as_uuid=True),
           primary_key=True,
           nullable=False,
           server_default=new_uuid),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('email', String, nullable=False),
    Column('password', String, nullable=False),
    Column('created_at', DateTime, nullable=False, **default_now),
    Column('updated_at', DateTime, nullable=False, onupdate=now,
           **default_now),
    Column('address_id',
           UUID(as_uuid=True),
           ForeignKey('address.id', name='fk_address_user'),
           nullable=False),
    UniqueConstraint('first_name',
                     'last_name',
                     'email',
                     name='unique_user_values'))

address = Table(
    'address', metadata,
    Column('id',
           UUID(as_uuid=True),
           primary_key=True,
           nullable=False,
           server_default=new_uuid), Column('name', String, nullable=False),
    Column('zip_code', String, nullable=False),
    Column('building_number', Integer, nullable=False),
    Column('street_name', String, nullable=False),
    Column('created_at', DateTime, nullable=False, **default_now),
    Column('updated_at', DateTime, nullable=False, onupdate=now,
           **default_now),
    UniqueConstraint('zip_code',
                     'building_number',
                     name='unique_address_values'))
