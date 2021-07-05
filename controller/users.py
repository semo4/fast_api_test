from uuid import UUID

from database import address, users
from fastapi import APIRouter, HTTPException
from model.model import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import delete, select, update

router = APIRouter()


@router.get('/users/', tags=['Users'])
async def read_users():
    try:
        result = select(users, address).join(address).where(
            users.c.address_id == address.c.id).execute()
        return {'message': 'data fetched successfully'}, 200, result.fetchall()
    except Exception as e:
        print(e)
        return HTTPException(detail='There is no data', status_code=204)


@router.get('/users/{user_id}', tags=['Users'])
async def read_single_user(user_id):
    try:
        result = select(users, address).join(address).where(
            users.c.address_id == address.c.id).where(
                users.c.id == user_id).execute()
        return {'message': 'data fetched successfully'}, 200, result.fetchone()
    except Exception as e:
        print(e)
        return {'message': 'There is no user with this Id'}, 404


@router.post('/users/', tags=['Users'])
async def add_new_users(user: User):
    try:
        user = dict(user)
        add = dict()
        add['name'] = user['name']
        del user['name']
        add['zip_code'] = user['zip_code']
        del user['zip_code']
        add['street_name'] = user['street_name']
        del user['street_name']
        add['building_number'] = user['building_number']
        del user['building_number']
        addres = address.insert().values(dict(add)).returning(
            address.c.id).execute()
        user['address_id'] = addres.first()[0]
        result = users.insert().values(user).returning(users.c.id).execute()
        return {'message': 'User Created Successfully'}, 201, result.first()
    except IntegrityError as e:
        print(e)
        return {'message': 'there is no data'}, 400


@router.put('/users/{user_id}', tags=['Users'])
async def update_single_user(user_id: UUID, user: User):
    try:
        user = dict(user)
        del user['name']
        del user['zip_code']
        del user['street_name']
        del user['building_number']
        result = update(users).where(users.c.id == user_id).values(
            dict(user)).returning(users.c.id, users.c.first_name,
                                  users.c.last_name).execute()
        return {'message': 'User Updated Successfully'}, 200, result.first()
    except IntegrityError as e:
        print(e)
        return {'message': 'The Id Dose not Exist'}, 400


@router.patch('/users/{user_id}', tags=['Users'])
async def update_single_value_user(user_id: UUID, user: User):
    try:
        user = dict(user)
        del user['name']
        del user['zip_code']
        del user['street_name']
        del user['building_number']
        result = update(users).where(users.c.id == user_id).values(
            dict(user)).returning(users.c.id).execute()
        return {'message': 'User Updated Successfully'}, 200, result.first()
    except IntegrityError as e:
        print(e)
        return {'message': 'The Id Dose not Exist'}, 400


@router.delete('/users/{user_id}', tags=['Users'])
async def delete_single_user(user_id):
    try:
        result = delete(users).where(users.c.id == user_id).returning(users.c.id).execute()
        return {'message': 'User Deleted Successfully'}, 200, result.first()
    except IntegrityError as e:
        print(e)
        return {'message': 'The Id Dose not Exist'}, 400


@router.get('/users/address/{address_id}', tags=['Users'])
async def read_single_user_by_address(address_id):
    try:
        result = select(users, address).join(address).where(
            users.c.address_id == address_id).execute()
        return {'message': 'data fetched successfully'}, 200, result.fetchone()
    except Exception as e:
        print(e)
        return {'message': 'There is no address with this Id'}, 404
