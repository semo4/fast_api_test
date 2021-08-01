from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse

from src.database import ALL_COLUMNS, address
from src.model import Address, AddressRespons, User
from src.oauth2 import get_current_user

router = APIRouter(prefix='/address',
                   tags=['Address'])


@router.get('/', response_model=AddressRespons)
async def get_addresses() -> JSONResponse:
    result = address.select().execute()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='There is No Addresses Found')

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            AddressRespons(**dict(i)) for i in result))


@router.get('/{address_id}', response_model=AddressRespons)
async def get_address_by_id(address_id: UUID) -> JSONResponse:
    result = address.select().where(
        address.c.id == address_id).execute().first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Address With this ID {} Not Found'.format(address_id))
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            AddressRespons(**dict(result))))


@router.post('/', response_model=AddressRespons)
async def add_new_address(address_: Address) -> JSONResponse:
    result = address.insert().values(
        dict(address_)).returning(ALL_COLUMNS).execute().first()

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(
                            AddressRespons(**dict(result))))


@router.delete('/{address_id}', response_model=AddressRespons)
async def delete(
        address_id: UUID) -> JSONResponse:

    result = address.select().where(
        address.c.id == address_id).execute().first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Address With this ID {} Not Found'.format(address_id))
    else:
        result = address.delete().where(address.c.id == address_id).returning(
            ALL_COLUMNS).execute().first()

        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,
                            content=jsonable_encoder(
                                AddressRespons(**dict(result))))


@router.put('/{address_id}', response_model=AddressRespons)
async def update(address_id: UUID, address_: Address) -> JSONResponse:
    result = address.select().where(
        address.c.id == address_id).execute().first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Address With this ID {} Not Found'.format(address_id))
    else:
        result = address.delete().where(address.c.id == address_id).returning(
            ALL_COLUMNS).execute().first()
        result = address.insert().values(
            dict(address_)).returning(ALL_COLUMNS).execute().first()

        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(
                                AddressRespons(**dict(result))))


@router.patch('/{address_id}', response_model=AddressRespons)
async def update_single_value(
        address_id: UUID, add: Address) -> JSONResponse:
    result = address.select().where(
        address.c.id == address_id).execute().first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Address With this ID {} Not Found'.format(address_id))
    else:
        result = address.update().where(address.c.id == address_id).values(
            dict(add.dict(
                exclude_unset=True))).returning(ALL_COLUMNS).execute().first()

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Address Dose Not Updated')

        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=jsonable_encoder(
                                AddressRespons(**dict(result))))
