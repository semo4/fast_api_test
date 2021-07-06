from uuid import UUID
from database import address, users
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.model.model import User, UserResponse
from sqlalchemy.sql import select

router = APIRouter()


@router.get('/users/', tags=['Users'], response_model=UserResponse)
async def read_users():
    result = select(users, address).select_from(
        users.join(address, users.c.address_id == address.c.id)).where(
            users.c.address_id == address.c.id).execute().fetchall()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No Users Found')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            UserResponse(**dict(i)) for i in result))


@router.get('/users/{user_id}', tags=['Users'], response_model=UserResponse)
async def read_single_user(user_id):
    result = select(users, address).select_from(
        users.join(address, users.c.address_id == address.c.id)).where(
            users.c.id == user_id).execute().fetchone()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User does not Exist')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(UserResponse(**dict(result))))


@router.post('/users/', tags=['Users'], response_model=UserResponse)
async def add_new_users(user: User):
    result = users.insert().values(dict(user)).returning(
        users.c.first_name, users.c.last_name,
        users.c.email).execute().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No User Addedd')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(UserResponse(**dict(result))))


@router.put('/users/{user_id}', tags=['Users'], response_model=UserResponse)
async def update_single_user(user_id: UUID, user: User):
    result = users.update().where(users.c.id == user_id).values(
        dict(user)).returning(users.c.id, users.c.first_name,
                              users.c.last_name,
                              users.c.email).execute().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User Update Failed')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(UserResponse(**dict(result))))


@router.patch('/users/{user_id}', tags=['Users'])
async def update_single_value_user(user_id: UUID, user: User):
    result = users.update().where(users.c.id == user_id).values(
        dict(user)).returning(users.c.first_name, users.c.last_name,
                              users.c.email).execute().first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User Update Failed')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(UserResponse(**dict(result))))


@router.delete('/users/{user_id}', tags=['Users'])
async def delete_single_user(user_id):
    result = users.delete().where(users.c.id == user_id).returning(
        users.c.id, users.c.first_name, users.c.last_name,
        users.c.email).execute().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User Dose not Found')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            [UserResponse(**dict(result))]))


@router.get('/users/address/{address_id}', tags=['Users'])
async def read_single_user_by_address(address_id):
    result = select(users, address).select_from(
        users.join(address, users.c.address_id == address.c.id)).where(
            users.c.address_id == address_id).execute().fetchone()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No User Found')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            [UserResponse(**dict(result))]))
