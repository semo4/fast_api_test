from datetime import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, ForeignKeyConstraint,
                        Integer, MetaData, String, Table, create_engine, func,
                        text)
from sqlalchemy.dialects.postgresql import UUID

DB_URL = 'postgresql://osama:yousef123@localhost:5432/user_address'

engine = create_engine(DB_URL, echo=True)
metadata = MetaData(bind=engine)

new_uuid = text('uuid_generate_v4()')
now = datetime.utcnow

default_now = dict(default=now, server_default=func.now())

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
    Column('created_at', DateTime, nullable=False, **default_now),
    Column('updated_at', DateTime, nullable=False, onupdate=now,
           **default_now),
    Column('address_id',
           UUID(as_uuid=True),
           ForeignKey('address.id'),
           nullable=False),
    ForeignKeyConstraint(['id'], ['address.id'], name='FK_ADDRESS_USER'))

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
           **default_now))
