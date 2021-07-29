from pytest_mock import MockFixture
import datetime
from uuid import UUID

headers_ = {
    'Authorization':
    'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvc0Bob3RtYWlsLmNvbSIsImV4cCI6MTYyNzU0Nzg0OH0.USBN7YFOapTDucQKNAk4guS3IXnYiCapmhi_Jyyn5U0'
}


def test_get_empty_users(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.engine.execute')
    mock_users.return_value.fetchall.return_value = []
    response = client.get('/users/', headers=headers_)
    assert response.status_code == 404


def test_get_users(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.engine.execute')
    # [(key0, value0), (key1, value1)]
    # mock_users.return_value.fetchall.return_value = [{
    #     "id": "1c85725c-b88d-497a-852b-a08028ba574f",
    #     "first_name": "osama",
    #     "last_name": "osama",
    #     "email": "os@hotmail.com",
    #     "created_at": "2021-07-18T13:39:47.640441",
    #     "updated_at": "2021-07-18T13:39:47.640448",
    #     "address_id": "add8fa65-08c1-4580-8700-d8f4ab35bdaf",
    #     "id_": "add8fa65-08c1-4580-8700-d8f4ab35bdaf",
    #     "name": "Amman",
    #     "zip_code": "12345",
    #     "building_number": 5,
    #     "street_name": "grtgrthggbg",
    #     "created_at_": "2021-07-18T13:39:10.648374",
    #     "updated_at_": "2021-07-18T13:39:10.648381"
    # }]
    mock_users.return_value.fetchall.return_value = [
        (UUID('f9d05432-9e45-4f5f-95c3-821f202c28df'), 'osama', 'osama',
         'os@hotmail.com',
         '$2b$12$YzDELF1mr5HKotPzHfsPzeanPBmnFtXAlUwbLxIwfJAsf2E92EvMe',
         datetime.datetime(2021, 7, 21, 18, 36, 39, 386103),
         datetime.datetime(2021, 7, 21, 18, 36, 39, 386112),
         UUID('29309b48-fff3-4b77-b07b-c4006e899fc1'),
         UUID('29309b48-fff3-4b77-b07b-c4006e899fc1'), 'Amman', '11111', 5,
         'mainstretamman', datetime.datetime(2021, 7, 21, 18, 35, 57, 928243),
         datetime.datetime(2021, 7, 21, 18, 35, 57, 928250))
    ]

    response = client.get('/users/', headers=headers_)
    assert response.status_code == 200


def test_get_user_by_wrong_id(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.engine.execute')
    mock_users.return_value.first.return_value = {}

    response = client.get('/users/1c85725c-b88d-497a-852b-a08028ba574f',
                          headers=headers_)
    assert response.status_code == 404


def test_get_user_by_id(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.engine.execute')
    mock_users.return_value.first.return_value = {
        "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
        "first_name": "osama",
        "last_name": "osama",
        "email": "os@hotmail.com",
        "created_at": "2021-07-18T13:39:47.640441",
        "updated_at": "2021-07-18T13:39:47.640448",
        "address_id": "add8fa65-08c1-4580-8700-d8f4ab35bdaf",
        "id_": "add8fa65-08c1-4580-8700-d8f4ab35bdaf",
        "name": "Amman",
        "zip_code": "12345",
        "building_number": 5,
        "street_name": "grtgrthggbg",
        "created_at_": "2021-07-18T13:39:10.648374",
        "updated_at_": "2021-07-18T13:39:10.648381"
    }

    response = client.get('/users/f9d05432-9e45-4f5f-95c3-821f202c28df',
                          headers=headers_)
    assert response.status_code == 200


def test_unauthorized(client):
    response = client.get('/users/')
    assert response.status_code == 401
    assert response.json() == {'message': 'Not UNAUTHORIZED'}


def test_post_user(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.users.insert')
    mock_users.return_value.values.return_value.returning.return_value.\
        execute.return_value.first.return_value = {
            "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
            "first_name": "osama10",
            "last_name": "osama10",
            "email": "osama@hotmail.com",
            "created_at": "2021-07-21T18:36:39.386103",
            "updated_at": "2021-07-21T18:36:39.386112",
            "address": {
                "id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
                "name": "Amman",
                "zip_code": "11111",
                "building_number": 5,
                "street_name": "mainstretamman",
                "created_at": "2021-07-21T18:35:57.928243",
                "updated_at": "2021-07-21T18:35:57.928250"
            }
        }
    result = {
        "first_name": "osama10",
        "last_name": "osama10",
        "email": "osama@hotmail.com",
        "address_id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
        "password": "123456789"
    }
    response = client.post('/users/', headers=headers_, json=result)
    assert response.status_code == 201


def test_post_user_with_missing_value(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.users.insert')
    mock_users.return_value.insert.return_value.values.return_value.\
        execute.return_value.first.return_value = {}
    result = {}
    response = client.post('/users/', headers=headers_, json=result)
    assert response.status_code == 422


def test_post_user_404(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.users.insert')
    mock_users.return_value.values.return_value.returning.return_value.\
        execute.return_value.first.return_value = {}
    result = {
        "first_name": "osama10",
        "last_name": "osama10",
        "email": "osama@hotmail.com",
        "address_id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
        "password": "123456789"
    }
    response = client.post('/users/', headers=headers_, json=result)
    assert response.status_code == 404


def test_delete_user(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.users.select')
    result = mock_users.return_value.where.return_value.execute.return_value.first.return_value = {
        "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
        "first_name": "osama10",
        "last_name": "osama10",
        "email": "os@hotmail.com",
        "created_at": "2021-07-21T18:36:39.386103",
        "updated_at": "2021-07-21T18:36:39.386112",
        "address": {
            "id_": "add8fa65-08c1-4580-8700-d8f4ab35bdaf",
            "name": "Amman",
            "zip_code": "12345",
            "building_number": 5,
            "street_name": "grtgrthggbg",
            "created_at_": "2021-07-18T13:39:10.648374",
            "updated_at_": "2021-07-18T13:39:10.648381"
        }
    }
    if result:
        mock_users = mocker.patch('controllers.users_controllers.users.delete')
        mock_users.return_value.where.return_value.returning.return_value.\
            execute.return_value.first.return_value = {
                "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
                "first_name": "osama",
                "last_name": "osama",
                "email": "os@hotmail.com",
                "created_at": "2021-07-21T18:36:39.386103",
                "updated_at": "2021-07-21T18:36:39.386112",
                "address": {
                    "id_": "add8fa65-08c1-4580-8700-d8f4ab35bdaf",
                    "name": "Amman",
                    "zip_code": "12345",
                    "building_number": 5,
                    "street_name": "grtgrthggbg",
                    "created_at_": "2021-07-18T13:39:10.648374",
                    "updated_at_": "2021-07-18T13:39:10.648381"
                }
            }
        response = client.delete('/users/f9d05432-9e45-4f5f-95c3-821f202c28df',
                                 headers=headers_)

        assert response.status_code == 204


def test_delete_user_wrong_id(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.engine.execute')
    mock_users.return_value.first.return_value = {}
    response = client.get('/users/f9d05432-9e45-4f5f-95c3-821f202c2847',
                          headers=headers_)
    assert response.status_code == 404


def test_delete_user_404(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.users.select')
    result = mock_users.return_value.where.return_value.execute.return_value.first.return_value = {
        "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
        "first_name": "osama",
        "last_name": "osama",
        "email": "os@hotmail.com",
        "created_at": "2021-07-21T18:36:39.386103",
        "updated_at": "2021-07-21T18:36:39.386112",
        "address": {
            "id_": "add8fa65-08c1-4580-8700-d8f4ab35bdaf",
            "name": "Amman",
            "zip_code": "12345",
            "building_number": 5,
            "street_name": "grtgrthggbg",
            "created_at_": "2021-07-18T13:39:10.648374",
            "updated_at_": "2021-07-18T13:39:10.648381"
        }
    }
    if result:
        mock_users = mocker.patch('controllers.users_controllers.users.delete')
        mock_users.return_value.where.return_value.returning.return_value.\
            execute.return_value.first.return_value = {}
        response = client.delete('/users/f9d05432-9e45-4f5f-95c3-821f202c2878',
                                 headers=headers_)
        assert response.status_code == 404


def test_put_user(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.users.select')
    result = mock_users.return_value.where.return_value.execute.return_value.first.return_value = {
        "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
        "first_name": "osama",
        "last_name": "osama",
        "email": "os@hotmail.com",
        "created_at": "2021-07-21T18:36:39.386103",
        "updated_at": "2021-07-21T18:36:39.386112",
        "address": {
            "id_": "add8fa65-08c1-4580-8700-d8f4ab35bdaf",
            "name": "Amman",
            "zip_code": "12345",
            "building_number": 5,
            "street_name": "grtgrthggbg",
            "created_at_": "2021-07-18T13:39:10.648374",
            "updated_at_": "2021-07-18T13:39:10.648381"
        }
    }
    if result:
        mock_users = mocker.patch('controllers.users_controllers.users.update')
        mock_users.return_value.where.return_value.values.return_value.returning.return_value.\
            execute.return_value.first.return_value = {
                "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
                "first_name": "osama10",
                "last_name": "osama10",
                "email": "os@hotmail.com",
                "created_at": "2021-07-21T18:36:39.386103",
                "updated_at": "2021-07-21T18:36:39.386112",
                "address": {}
            }
        result = {
            "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
            "first_name": "osama10",
            "last_name": "osama10",
            "email": "os@hotmail.com",
            "address_id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
            "password": "123456789"
        }
        response = client.put('/users/f9d05432-9e45-4f5f-95c3-821f202c28df',
                              headers=headers_,
                              json=result)
        assert response.status_code == 201


def test_put_user_wrong_id(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.users.select')
    result = mock_users.return_value.where.return_value.execute.return_value.first.return_value = {
        "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
        "first_name": "osama",
        "last_name": "osama",
        "email": "os@hotmail.com",
        "created_at": "2021-07-21T18:36:39.386103",
        "updated_at": "2021-07-21T18:36:39.386112",
        "address": {
            "id_": "add8fa65-08c1-4580-8700-d8f4ab35bdaf",
            "name": "Amman",
            "zip_code": "12345",
            "building_number": 5,
            "street_name": "grtgrthggbg",
            "created_at_": "2021-07-18T13:39:10.648374",
            "updated_at_": "2021-07-18T13:39:10.648381"
        }
    }
    if result:
        mock_users = mocker.patch('controllers.users_controllers.users.update')
        mock_users.return_value.where.return_value.values.return_value.returning.return_value.\
            execute.return_value.first.return_value = {
            }
        result = {
            "first_name": "osama10",
            "last_name": "osama10",
            "email": "os@hotmail.com",
            "address_id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
            "password": "123456789"
        }
        response = client.put('/users/3fa85f64-5717-4562-b3fc-2c963f66afa6',
                              headers=headers_,
                              json=result)
        assert response.status_code == 404


def test_put_user_missing_value(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.users.update')
    mock_users.return_value.where.return_value.values.return_value.returning.return_value.\
        execute.return_value.first.return_value = {
            "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
            "first_name": "osama10",
            "last_name": "osama10",
            "email": "os@hotmail.com",
            "created_at": "2021-07-21T18:36:39.386103",
            "updated_at": "2021-07-21T18:36:39.386112",
            "address": {}
        }
    result = {
        "last_name": "osama10",
        "email": "os@hotmail.com",
        "address_id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
        "password": "123456789"
    }
    response = client.put('/users/f9d05432-9e45-4f5f-95c3-821f202c28df',
                          headers=headers_,
                          json=result)
    assert response.status_code == 422


def test_put_user_404(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.users.select')
    result = mock_users.return_value.where.return_value.execute.return_value.first.return_value = {
        "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
        "first_name": "osama",
        "last_name": "osama",
        "email": "os@hotmail.com",
        "created_at": "2021-07-21T18:36:39.386103",
        "updated_at": "2021-07-21T18:36:39.386112",
        "address": {
            "id_": "add8fa65-08c1-4580-8700-d8f4ab35bdaf",
            "name": "Amman",
            "zip_code": "12345",
            "building_number": 5,
            "street_name": "grtgrthggbg",
            "created_at_": "2021-07-18T13:39:10.648374",
            "updated_at_": "2021-07-18T13:39:10.648381"
        }
    }
    if result:
        mock_users = mocker.patch('controllers.users_controllers.users.update')
        mock_users.return_value.where.return_value.values.return_value.returning.return_value.\
            execute.return_value.first.return_value = {}
        result = {
            "first_name": "osama10",
            "last_name": "osama10",
            "email": "os@hotmail.com",
            "address_id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
            "password": "123456789"
        }
        response = client.put('/users/f9d05432-9e45-4f5f-95c3-821f202c28df',
                              headers=headers_,
                              json=result)
        assert response.status_code == 404


def test_patch_user(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.users.select')
    result = mock_users.return_value.where.return_value.execute.return_value.first.return_value = {
        "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
        "first_name": "osama",
        "last_name": "osama",
        "email": "os@hotmail.com",
        "created_at": "2021-07-21T18:36:39.386103",
        "updated_at": "2021-07-21T18:36:39.386112",
        "address": {
            "id_": "add8fa65-08c1-4580-8700-d8f4ab35bdaf",
            "name": "Amman",
            "zip_code": "12345",
            "building_number": 5,
            "street_name": "grtgrthggbg",
            "created_at_": "2021-07-18T13:39:10.648374",
            "updated_at_": "2021-07-18T13:39:10.648381"
        }
    }
    if result:
        mock_users = mocker.patch('controllers.users_controllers.users.update')
        mock_users.return_value.where.return_value.values.return_value.returning.return_value.\
            execute.return_value.first.return_value = {
                "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
                "first_name": "osama10",
                "last_name": "osama10",
                "email": "os@hotmail.com",
                "created_at": "2021-07-21T18:36:39.386103",
                "updated_at": "2021-07-21T18:36:39.386112",
                "address": {}
            }
        result = {
            "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
            "first_name": "osama10",
            "last_name": "osama10",
            "email": "os@hotmail.com",
            "address_id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
            "password": "123456789"
        }
        response = client.patch('/users/f9d05432-9e45-4f5f-95c3-821f202c28df',
                                headers=headers_,
                                json=result)
        assert response.status_code == 201


def test_patch_user_wrong_id(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.users.select')
    result = mock_users.return_value.where.return_value.execute.return_value.first.return_value = {
        "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
        "first_name": "osama",
        "last_name": "osama",
        "email": "os@hotmail.com",
        "created_at": "2021-07-21T18:36:39.386103",
        "updated_at": "2021-07-21T18:36:39.386112",
        "address": {
            "id_": "add8fa65-08c1-4580-8700-d8f4ab35bdaf",
            "name": "Amman",
            "zip_code": "12345",
            "building_number": 5,
            "street_name": "grtgrthggbg",
            "created_at_": "2021-07-18T13:39:10.648374",
            "updated_at_": "2021-07-18T13:39:10.648381"
        }
    }
    if result:
        mock_users = mocker.patch('controllers.users_controllers.users.update')
        mock_users.return_value.where.return_value.values.return_value.returning.return_value.\
            execute.return_value.first.return_value = {
            }
        result = {
            "first_name": "osama10",
            "last_name": "osama10",
            "email": "os@hotmail.com",
            "address_id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
            "password": "123456789"
        }
        response = client.patch('/users/3fa85f64-5717-4562-b3fc-2c963f66afa6',
                                headers=headers_,
                                json=result)
        assert response.status_code == 404


def test_patch_user_missing_value(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.users.update')
    mock_users.return_value.where.return_value.values.return_value.returning.return_value.\
        execute.return_value.first.return_value = {
            "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
            "first_name": "osama10",
            "last_name": "osama10",
            "email": "os@hotmail.com",
            "created_at": "2021-07-21T18:36:39.386103",
            "updated_at": "2021-07-21T18:36:39.386112",
            "address": {}
        }
    result = {
        "last_name": "osama10",
        "email": "os@hotmail.com",
        "address_id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
        "password": "123456789"
    }
    response = client.patch('/users/f9d05432-9e45-4f5f-95c3-821f202c28df',
                            headers=headers_,
                            json=result)
    assert response.status_code == 422


def test_patch_user_404(client, mocker: MockFixture):
    mock_users = mocker.patch('controllers.users_controllers.users.select')
    result = mock_users.return_value.where.return_value.execute.return_value.first.return_value = {
        "id": "f9d05432-9e45-4f5f-95c3-821f202c28df",
        "first_name": "osama",
        "last_name": "osama",
        "email": "os@hotmail.com",
        "created_at": "2021-07-21T18:36:39.386103",
        "updated_at": "2021-07-21T18:36:39.386112",
        "address": {
            "id_": "add8fa65-08c1-4580-8700-d8f4ab35bdaf",
            "name": "Amman",
            "zip_code": "12345",
            "building_number": 5,
            "street_name": "grtgrthggbg",
            "created_at_": "2021-07-18T13:39:10.648374",
            "updated_at_": "2021-07-18T13:39:10.648381"
        }
    }
    if result:
        mock_users = mocker.patch('controllers.users_controllers.users.update')
        mock_users.return_value.where.return_value.values.return_value.returning.return_value.\
            execute.return_value.first.return_value = {}
        result = {
            "first_name": "osama10",
            "last_name": "osama10",
            "email": "os@hotmail.com",
            "address_id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
            "password": "123456789"
        }
        response = client.patch('/users/f9d05432-9e45-4f5f-95c3-821f202c28df',
                                headers=headers_,
                                json=result)
        assert response.status_code == 404
