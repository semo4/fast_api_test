from uuid import UUID

from database import address
from fastapi import APIRouter, HTTPException
from model.model import Address
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import delete, select, update

router = APIRouter()


@router.get('/address/', tags=['Address'])
async def read_addresses():
    try:
        result = select(address).execute()
        return {'message': 'data fetched successfully'}, 200, result.fetchall()
    except Exception as e:
        print(e)
        return {'message': 'There is no data'}, 204


@router.get('/address/{address_id}', tags=['Address'])
async def read_single_address(address_id):
    try:
        result = select(address).where(address.c.id == address_id).execute()
        return {'message': 'data fetched successfully'}, 200, result.fetchone()
    except Exception as e:
        print(e)
        return {'message': 'There is no address with this Id'}, 404


@router.post('/address/', tags=['Address'])
async def add_new_address(add: Address):
    try:
        result = address.insert().values(dict(add)).returning(
            address.c.id, address.c.name).execute()
        return HTTPException(detail='Address Created Successfully',
                             status_code=200), result.first()
    except IntegrityError as e:
        print(e)
        return {'message': 'there is no data'}, 400


@router.put('/address/{address_id}', tags=['Address'])
async def update_single_address(address_id: UUID, add: Address):
    try:
        result = update(address).where(address.c.id == address_id).values(
            dict(add)).returning(address.c.id).execute()
        return {'message': 'Address Updated Successfully'}, 200, result.first()
    except IntegrityError as e:
        print(e)
        return {'message': 'The Id Dose not Exist'}, 400


@router.patch('/address/{address_id}', tags=['Address'])
async def update_single_value_address(address_id: UUID, add: Address):
    try:
        result = update(address).where(address.c.id == address_id).values(
            dict(add)).returning(address.c.id).execute()
        return {'message': 'Address Updated Successfully'}, 200, result.first()
    except IntegrityError as e:
        print(e)
        return {'message': 'The Id Dose not Exist'}, 400


@router.delete('/address/{address_id}', tags=['Address'])
async def delete_single_address(address_id):
    try:
        result = delete(address).where(address.c.id == address_id).returning(
            address.c.id).execute()
        return {'message': 'Address Deleted Successfully'}, 200, result.first()
    except IntegrityError as e:
        print(e)
        return {'message': 'The Id Dose not Exist'}, 400
