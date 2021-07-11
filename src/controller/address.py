from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.sql.elements import literal_column

from src.database import address
from src.model import Address, AddressRespons

router = APIRouter(prefix='/address', tags=['Address'])


def address_by_id(address_id: UUID):
    result = address.select().where(
        address.c.id == address_id).execute().first()
    return result


@router.get('/', response_model=AddressRespons)
async def get_addresses():
    result = address.select().execute().fetchall()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No Addresses Found')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            AddressRespons(**dict(i)) for i in result))


@router.get('/{address_id}', response_model=AddressRespons)
async def get_address_by_id(address_id: UUID):
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
async def add_new_address(add: Address):
    result = address.insert().values(dict(add)).returning(
        literal_column('*')).execute().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Address Not Created')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            AddressRespons(**dict(result))))


@router.delete('/{address_id}', response_model=AddressRespons)
async def delete(address_id: UUID):
    result = address_by_id(address_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Address With this ID {} Not Found'.format(address_id))
    else:
        result = address.delete().where(address.c.id == address_id).returning(
            literal_column('*')).execute().first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Address Not Deleted')
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(
                                AddressRespons(**dict(result))))


@router.put('/{address_id}', response_model=AddressRespons)
async def update(address_id: UUID, add: Address):
    result = address_by_id(address_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Address With this ID {} Not Found'.format(address_id))
    else:
        result = address.update().where(address.c.id == address_id).values(
            dict(add)).returning(literal_column('*')).execute().first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Address Dose Not Updated')
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(
                                AddressRespons(**dict(result))))


@router.patch('/{address_id}', response_model=AddressRespons)
async def update_single_value_address(address_id: UUID, add: Address):
    result = address_by_id(address_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Address With this ID {} Not Found'.format(address_id))
    else:
        result = address.update().where(address.c.id == address_id).values(
            dict(add.dict(exclude_unset=True))).returning(literal_column('*')).execute().first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Address Dose Not Updated')
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(
                                AddressRespons(**dict(result))))
