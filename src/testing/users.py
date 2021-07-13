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
    'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvc0Bob3RtYWlsLmNvbSIsImV4cCI6MTYyNjE2OTA4MX0.6SdePgjTiO7sGxeSNVKXUOmbFKKrvfEY329u7HlvG4A'
}


@pytest.mark.asyncio
async def test_get_all_users():
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000/users', headers=headers_) as ac:
        response = await ac.get('/')
    data = requests.get('http://127.0.0.1:8000/users/', headers=headers_)
    assert response.status_code == data.status_code
    assert response.json() == data.json()


@pytest.mark.asyncio
async def test_get_user_by_id():
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000/users', headers=headers_) as ac:
        response = await ac.get('/{31b89895-249c-4f5e-9d19-7732e78aa851}')
    data = requests.get('http://127.0.0.1:8000/users/{31b89895-249c-4f5e-9d19-7732e78aa851}',
                        headers=headers_)
    assert response.status_code == data.status_code
    assert response.json() == data.json()


post_user = {
    "first_name": "ffnewstring",
    "last_name": "ffnewstring",
    "email": "ffnewstring@hotmail.com",
    "address_id": "a3d1918d-9420-451f-9d25-1f9313d7891c",
    "password": "123456789"
}


@pytest.mark.asyncio
async def test_post():
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000/users') as ac:
        response = await ac.post('/', data=json.dumps(post_user))
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_delete():
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000/users', headers=headers_) as ac:
        response = await ac.delete('/{8bd63f37-21b7-48f6-b126-38d40998cf4e}')
    assert response.status_code == 204


put_user = {
    "first_name": "testput",
    "last_name": "testput",
    "email": "testput@hotmail.com",
    "address_id": "a3d1918d-9420-451f-9d25-1f9313d7891c",
    "password": "123456789"
}


@pytest.mark.asyncio
async def test_put():
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000/users', headers=headers_) as ac:
        response = await ac.put('/{75fcd62d-9e28-4aef-b210-d157a0f62a2f}', data=json.dumps(put_user))
    assert response.status_code == 201


patch_user = {
    "first_name": "newtestput",
    "last_name": "newtestput",
    "email": "newtestput@hotmail.com",
    "address_id": "a3d1918d-9420-451f-9d25-1f9313d7891c",
    "password": "123456789"
}


@pytest.mark.asyncio
async def test_patch():
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000/users', headers=headers_) as ac:
        response = await ac.patch('/{75fcd62d-9e28-4aef-b210-d157a0f62a2f}', data=json.dumps(patch_user))
    assert response.status_code == 201
