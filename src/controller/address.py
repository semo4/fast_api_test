from uuid import UUID

from database import address
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.model.model import Address, AddressRespons

router = APIRouter()


@router.get('/address/', tags=['Address'], response_model=AddressRespons)
async def read_addresses():
    result = address.select().execute().fetchall()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No Address found')
    data = jsonable_encoder(result)
    print(data)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            AddressRespons(**dict(i)) for i in result))


@router.get('/address/{address_id}',
            tags=['Address'],
            response_model=AddressRespons)
async def read_single_address(address_id):

    result = address.select().where(
        address.c.id == address_id).execute().fetchone()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No Address found')

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            AddressRespons(**dict(result))))


@router.post('/address/', tags=['Address'], response_model=AddressRespons)
async def add_new_address(add: Address):
    result = address.insert().values(dict(add)).returning(
        address.c.id, address.c.name, address.c.zip_code,
        address.c.building_number, address.c.street_name).execute().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_ERROR,
                            detail='No Address found')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            AddressRespons(**dict(result))))


@router.put('/address/{address_id}',
            tags=['Address'],
            response_model=AddressRespons)
async def update_single_address(address_id: UUID, add: Address):
    result = address.update().where(address.c.id == address_id).values(
        dict(add)).returning(address.c.id, address.c.name, address.c.zip_code,
                             address.c.building_number,
                             address.c.street_name).execute().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_ERROR,
                            detail='No Address found')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            AddressRespons(**dict(result))))


@router.patch('/address/{address_id}',
              tags=['Address'],
              response_model=AddressRespons)
async def update_single_value_address(address_id: UUID, add: Address):
    result = address.update().where(address.c.id == address_id).values(
        dict(add)).returning(address.c.id, address.c.name, address.c.zip_code,
                             address.c.building_number,
                             address.c.street_name).execute().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_ERROR,
                            detail='No Address found')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            AddressRespons(**dict(result))))


@router.delete('/address/{address_id}', tags=['Address'])
async def delete_single_address(address_id):

    result = address.delete().where(address.c.id == address_id).returning(
        address.c.id, address.c.name, address.c.zip_code,
        address.c.building_number, address.c.street_name).execute().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_ERROR,
                            detail='No Address found')
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            AddressRespons(**dict(result))))
