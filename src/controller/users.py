from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.sql.elements import literal_column

from src.database import address, users
from src.model import User, UserResponse

router = APIRouter(prefix='/users', tags=['Users'])


def user_by_id(user_id: UUID):
    result = users.select().where(users.c.id == user_id).execute().first()
    return result


@router.get('/', response_model=UserResponse)
async def get_users():
    result = select([users, address]).select_from(
        users.join(address, users.c.address_id == address.c.id)).where(
            users.c.address_id == address.c.id).execute().fetchall()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No Users Found')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            UserResponse(**dict(i)) for i in result))


@router.get('/{user_id}', response_model=UserResponse)
async def get_user_by_id(user_id: UUID):
    result = select(users, address).select_from(
        users.join(address, users.c.address_id == address.c.id)).where(
            users.c.id == user_id).execute().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User does not Exist')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(UserResponse(**dict(result))))


@router.post('/', response_model=UserResponse)
async def add_new_users(user: User):
    result = users.insert().values(dict(user)).returning(
        literal_column('*')).execute().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No User Addedd')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(UserResponse(**dict(result))))


@router.delete('/{user_id}', response_model=UserResponse)
async def delete_user_by_id(user_id: UUID):
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
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(
                                [UserResponse(**dict(result))]))


@router.put('/{user_id}', response_model=UserResponse)
async def update_single_user(user_id: UUID, user: User):
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
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(
                                UserResponse(**dict(result))))


@router.patch('/{user_id}', response_model=UserResponse)
async def update_single_value_user(user_id: UUID, user: User):
    result = user_by_id(user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User Not Found With this {}'.format(user_id))
    else:
        result = users.update().where(users.c.id == user_id).values(
            dict(user.dict(exclude_unset=True))).returning(literal_column('*')).execute().first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User Not Update with values {}'.format(user))
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(
                                UserResponse(**dict(result))))
