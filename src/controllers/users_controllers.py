from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import select

from src.database import ALL_COLUMNS, address, engine, users
from src.hashpass import Hash
from src.model import User, UserResponse
from src.oauth2 import get_current_user

router = APIRouter(prefix='/users', tags=['Users'])
# current_user: User = Depends(get_current_user)


@router.get('/', response_model=UserResponse)
async def get_users() -> JSONResponse:
    stmt = select([users, address]).select_from(
        users.join(address, users.c.address_id == address.c.id)).where(
            users.c.address_id == address.c.id)
    result = engine.execute(stmt).fetchall()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No Users Found')
    user = list()
    for rowproxy in result:
        data = dict()
        data['id'] = rowproxy[0]
        data['first_name'] = rowproxy[1]
        data['last_name'] = rowproxy[2]
        data['email'] = rowproxy[3]
        data['created_at'] = rowproxy[5]
        data['updated_at'] = rowproxy[6]
        data_address = dict()
        data_address['id'] = rowproxy[7]
        data_address['name'] = rowproxy[9]
        data_address['zip_code'] = rowproxy[10]
        data_address['building_number'] = rowproxy[11]
        data_address['street_name'] = rowproxy[12]
        data_address['created_at'] = rowproxy[13]
        data_address['updated_at'] = rowproxy[14]
        data['address'] = data_address
        user.append(data)

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            UserResponse(**dict(i)) for i in user))


@router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(user_id: UUID) -> JSONResponse:
    stmt = select(users, address).select_from(
        users.join(
            address,
            users.c.address_id == address.c.id)).where(users.c.id == user_id)
    result = engine.execute(stmt).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User does not Exist')
    data = dict()
    data['id'] = result['id']
    data['first_name'] = result['first_name']
    data['last_name'] = result['last_name']
    data['email'] = result['email']
    data['created_at'] = result['created_at']
    data['updated_at'] = result['updated_at']
    data_address = dict()
    data_address['id'] = result['id']
    data_address['name'] = result['name']
    data_address['zip_code'] = result['zip_code']
    data_address['building_number'] = result['building_number']
    data_address['street_name'] = result['street_name']
    data_address['created_at'] = result['created_at']
    data_address['updated_at'] = result['updated_at']
    data['address'] = data_address

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(UserResponse(**dict(data))))


@router.post('/', response_model=UserResponse)
async def add_new_users(user: User) -> JSONResponse:
    user.password = Hash.hashing_pass(user.password)

    result = users.insert().values(
        dict(user)).returning(ALL_COLUMNS).execute().first()
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(UserResponse(**dict(result))))


@router.delete('/{user_id}', response_model=UserResponse)
async def delete_user_by_id(user_id: UUID
                            ) -> JSONResponse:
    result = users.select().where(users.c.id == user_id).execute().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User Dose not Found')
    else:
        result = users.delete().where(
            users.c.id == user_id).returning(ALL_COLUMNS).execute().first()
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,
                            content=jsonable_encoder(
                                UserResponse(**dict(result))))


@router.put('/{user_id}', response_model=UserResponse)
async def update_single_user(user_id: UUID, user: User
                             ) -> JSONResponse:
    result = users.select().where(users.c.id == user_id).execute().first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User Not Found With this {}'.format(user_id))
    else:
        result = users.delete().where(
            users.c.id == user_id).returning(ALL_COLUMNS).execute().first()

        user.password = Hash.hashing_pass(user.password)
        result = users.insert().values(
            dict(user)).returning(ALL_COLUMNS).execute().first()

        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(
                                UserResponse(**dict(result))))


@router.patch('/{user_id}', response_model=UserResponse)
async def update_single_value_user(user_id: UUID, user: User
                                   ) -> JSONResponse:
    result = users.select().where(users.c.id == user_id).execute().first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User Not Found With this {}'.format(user_id))
    else:
        result = users.update().where(users.c.id == user_id).values(
            dict(user.dict(
                exclude_unset=True))).returning(ALL_COLUMNS).execute().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User Not Update with values {}'.format(user))

        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(
                                UserResponse(**dict(result))))
