import pytest
from fastapi.testclient import TestClient
import os
import sys
sys.path.append(os.getcwd())
from app import app


headers_ = {
    'Authorization':
    'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvc0Bob3RtYWlsLmNvbSIsImV4cCI6MTYyNjI2Nzk3NH0.t03ccrjKZZ0MjYn0Q4Yt38xUK7FmGKmNYGSAt7oBd2s'
}


@pytest.fixture(scope="module")
def client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
def get_users(client):
    data = client.get('/users/', headers=headers_)
    return data


@pytest.fixture(scope="module")
def single_user(client):
    data = client.get('/users/', headers=headers_)
    if data.status_code == 401:
        return data
    data = client.get('/users/' + data.json()[0]['id'], headers=headers_)
    return data


@pytest.fixture(scope="module")
def unauthorize_user(client):
    data = client.get('/users/')
    return data


@pytest.fixture(scope="module")
def post_user():
    post_user = {
        "first_name": "pytestuser",
        "last_name": "pytestuser",
        "email": "pytestuser@hotmail.com",
        "address_id": "a3d1918d-9420-451f-9d25-1f9313d7891c",
        "password": "123456789"
    }
    return post_user


@pytest.fixture(scope="module")
def delete_user(client):
    data = client.get('/users/', headers=headers_)
    if data.status_code == 401:
        return data
    data = client.get('/users/' + data.json()[len(data.json()) - 1]['id'],
                      headers=headers_)
    return data


@pytest.fixture(scope="module")
def put_data():
    put_user = {
        "first_name": "updatepytest",
        "last_name": "updatepytest",
        "email": "updatepytest@hotmail.com",
        "address_id": "a3d1918d-9420-451f-9d25-1f9313d7891c",
        "password": "123456789"
    }
    return put_user


@pytest.fixture(scope="module")
def get_addresses(client):
    data = client.get('/address/', headers=headers_)
    return data


@pytest.fixture(scope="module")
def unauthorize_address(client):
    data = client.get('/address/')
    return data


@pytest.fixture(scope="module")
def single_address(client):
    data = client.get('/address/', headers=headers_)
    if data.status_code == 401:
        return data
    data = client.get('/address/' + data.json()[0]['id'], headers=headers_)
    return data


@pytest.fixture(scope="module")
def post_address():
    post_address = {
        "name": "Aqaba",
        "zip_code": "45696",
        "building_number": "7",
        "street_name": "mainstreet"
    }
    return post_address


@pytest.fixture(scope="module")
def delete_address(client):
    data = client.get('/address/', headers=headers_)
    if data.status_code == 401:
        return data
    data = client.get('/address/' + data.json()[len(data.json()) - 1]['id'],
                      headers=headers_)
    return data


@pytest.fixture(scope="module")
def put_address():
    put_data = {
        "name": "Aqaba55",
        "zip_code": "10236",
        "building_number": "10",
        "street_name": "putmainstreet"
    }
    return put_data
