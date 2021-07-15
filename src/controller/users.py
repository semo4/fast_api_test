from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.sql.elements import literal_column

from src.database import address, users
from src.hashpass import Hash
from src.model import User, UserResponse
from src.oauth2 import get_current_user


router = APIRouter(prefix='/users', tags=['Users'])


def user_by_id(user_id: UUID):
    result = users.select().where(users.c.id == user_id).execute().first()
    return result


def get_users_data(result):
    user = list()
    for i in result:
        data = dict()
        data['id'] = i[0]
        data['first_name'] = i[1]
        data['last_name'] = i[2]
        data['email'] = i[3]
        data['created_at'] = i[5]
        data['updated_at'] = i[6]
        data_address = dict()
        data_address['id'] = i[8]
        data_address['name'] = i[9]
        data_address['zip_code'] = i[10]
        data_address['building_number'] = i[11]
        data_address['street_name'] = i[12]
        data_address['created_at'] = i[13]
        data_address['updated_at'] = i[14]
        data['address'] = data_address
        user.append(data)
    return user


@router.get('/', response_model=UserResponse)
async def get_users(current_user: User = Depends(
        get_current_user)) -> JSONResponse:
    result = select([users, address]).select_from(
        users.join(address, users.c.address_id == address.c.id)).where(
            users.c.address_id == address.c.id).execute().fetchall()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No Users Found')
    user = get_users_data(result)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            UserResponse(**dict(i)) for i in user))


@router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(user_id: UUID,
                         current_user: User = Depends(get_current_user)) -> JSONResponse:
    result = select(users, address).select_from(
        users.join(address, users.c.address_id == address.c.id)).where(
            users.c.id == user_id).execute().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User does not Exist')
    data = dict()
    data['id'] = result[0]
    data['first_name'] = result[1]
    data['last_name'] = result[2]
    data['email'] = result[3]
    data['created_at'] = result[5]
    data['updated_at'] = result[6]
    data_address = dict()
    data_address['id'] = result[8]
    data_address['name'] = result[9]
    data_address['zip_code'] = result[10]
    data_address['building_number'] = result[11]
    data_address['street_name'] = result[12]
    data_address['created_at'] = result[13]
    data_address['updated_at'] = result[14]
    data['address'] = data_address

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(UserResponse(**dict(data))))


@router.post('/', response_model=UserResponse)
async def add_new_users(user: User) -> JSONResponse:
    user.password = Hash.hashing_pass(user.password)
    result = users.insert().values(dict(user)).returning(
        literal_column('*')).execute().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No User Addedd')
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(UserResponse(**dict(result))))


@router.delete('/{user_id}', response_model=UserResponse)
async def delete_user_by_id(user_id: UUID,
                            current_user: User = Depends(get_current_user)) -> JSONResponse:
    result = user_by_id(user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User Dose not Found')
    else:
        result = users.delete().where(users.c.id == user_id).returning(
            literal_column('*')).execute().first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='User Dose not deleted')
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,
                            content=jsonable_encoder(
                                UserResponse(**dict(result))))


@router.put('/{user_id}', response_model=UserResponse)
async def update_single_user(user_id: UUID, user: User,
                             current_user: User = Depends(get_current_user)) -> JSONResponse:
    result = user_by_id(user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User Not Found With this {}'.format(user_id))
    else:
        result = users.update().where(users.c.id == user_id).values(
            dict(user)).returning(literal_column('*')).execute().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User Not Update with values {}'.format(user))
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(
                                UserResponse(**dict(result))))


@router.patch('/{user_id}', response_model=UserResponse)
async def update_single_value_user(user_id: UUID, user: User,
                                   current_user: User = Depends(get_current_user)) -> JSONResponse:
    result = user_by_id(user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User Not Found With this {}'.format(user_id))
    else:
        result = users.update().where(users.c.id == user_id).values(
            dict(user.dict(exclude_unset=True))).returning(
                literal_column('*')).execute().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User Not Update with values {}'.format(user))
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(
                                UserResponse(**dict(result))))
