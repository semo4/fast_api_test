import pytest
import requests
from httpx import AsyncClient
import os
import sys
import json
sys.path.append(os.getcwd())
from app import app


headers_ = {
    'Authorization':
    'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvc0Bob3RtYWlsLmNvbSIsImV4cCI6MTYyNjE2ODEyMn0.fXSJDUK5lGGze6_AqGVgAywxwpu-nuYe1uRNQoAUahk'
}


@pytest.mark.asyncio
async def test_get_all_address():
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000/address', headers=headers_) as ac:
        response = await ac.get('/')
    data = requests.get('http://127.0.0.1:8000/address/', headers=headers_)
    assert response.status_code == data.status_code
    assert response.json() == data.json()


@pytest.mark.asyncio
async def test_get_user_by_id():
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000/address', headers=headers_) as ac:
        response = await ac.get('/{a3d1918d-9420-451f-9d25-1f9313d7891c}')
    data = requests.get('http://127.0.0.1:8000/address/{a3d1918d-9420-451f-9d25-1f9313d7891c}',
                        headers=headers_)
    assert response.status_code == data.status_code
    assert response.json() == data.json()


post_address = {
  "name": "Aqapa",
  "zip_code": "44758",
  "building_number": "55",
  "street_name": "ghrfgvddvsklvofvnsf"
}

@pytest.mark.asyncio
async def test_post():
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000/address', headers=headers_) as ac:
        response = await ac.post('/', data=json.dumps(post_address))
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_delete():
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000/address', headers=headers_) as ac:
        response = await ac.delete('/{c8f4f309-94e8-4a9c-82e1-ced4193386a6}')
    assert response.status_code == 204


put_address = {
  "name": "Aqapa",
  "zip_code": "44758",
  "building_number": "55",
  "street_name": "ghrfgvddvsklvofvnsf"
}

@pytest.mark.asyncio
async def test_update():
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000/address', headers=headers_) as ac:
        response = await ac.put('/{d80a0cf5-af54-4339-90a0-cad6868c0f92}', data=json.dumps(put_address))
    assert response.status_code == 201


patch_address = {
  "name": "Irbid",
  "zip_code": "44758"
}


@pytest.mark.asyncio
async def test_update():
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000/address', headers=headers_) as ac:
        response = await ac.put('/{d80a0cf5-af54-4339-90a0-cad6868c0f92}', data=json.dumps(patch_address))
    assert response.status_code == 201
