from pytest_mock import MockFixture

headers_ = {
    'Authorization':
    'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvc0Bob3RtYWlsLmNvbSIsImV4cCI6MTYyNjM2MzQ3Mn0.rwbX1NXzqz5vNYS6EE7HU4CXkvyhUv7jRfNTjGt02so'
}


def test_get_users(client, mocker: MockFixture):
    mock_users = mocker.patch('controller.users.users')
    result = mock_users.return_value.select.return_value.select_from.return_value.where.return_value.execute.return_value.fetchall.return_value = {
        'first_name': 'pytestuser'
    }
    mock_users.called == True
    response = client.get('/users/', headers=headers_)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    elif response.status_code == 404:
        assert response.status_code == 404
        assert response.json() == {'message': 'Not Exist'}
    else:
        assert response.status_code == 200
        assert response.json()[0]['first_name'] == result['first_name']


def test_unauthorize_get_users(client):
    response = client.get('/users/')
    assert response.status_code == 401
    assert response.json() == {'message': 'Not UNAUTHORIZED'}


def test_get_user_by_id(client, mocker: MockFixture):
    mock_users = mocker.patch('controller.users.users')
    result = mock_users.return_value.select.return_value.select_from.return_value.where.return_value.execute.return_value.fetchall.return_value = {
        "id": "1fe4ab08-af2c-4ec6-966c-ed9736270b4c",
        "first_name": "ahmad",
        "last_name": "ahmad",
        "email": "ah10@hotmail.com",
        "created_at": "2021-07-12T12:17:34.419524",
        "updated_at": "2021-07-12T12:17:34.419531",
        "address": {
            "id": "a3d1918d-9420-451f-9d25-1f9313d7891c",
            "name": "Amman",
            "zip_code": "77777",
            "building_number": 41,
            "street_name": "fbwtbwrtbgfgbtrbA",
            "created_at": "2021-07-12T07:11:57.908966",
            "updated_at": "2021-07-12T07:11:57.908974"
        }
    }
    mock_users.called == True
    response = client.get('/users/' + result['id'], headers=headers_)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    elif response.status_code == 400:
        assert response.status_code == 400
        assert response.json()['message'] == 'violates constraint'
    else:
        assert response.status_code == 200
        assert response.json()['email'] == result['email']


def test_get_user_not_exist(client, mocker: MockFixture):
    mock_users = mocker.patch('controller.users.users')
    result = mock_users.return_value.select.return_value.select_from.return_value.where.return_value.execute.return_value.fetchall.return_value = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "first_name": "string",
        "last_name": "string",
        "email": "string",
        "created_at": "2021-07-15T13:57:17.197Z",
        "updated_at": "2021-07-15T13:57:17.197Z",
        "address": {}
    }
    mock_users.called == True
    response = client.get('/users/' + result['id'], headers=headers_)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    else:
        assert response.status_code == 404
        assert response.json() == {'message': 'Not Exist'}


def test_get_user_wrong_id(client, mocker: MockFixture):
    mock_users = mocker.patch('controller.users.users')
    result = mock_users.return_value.select.return_value.select_from.return_value.where.return_value.execute.return_value.fetchall.return_value = {
        "id": "1fe4ab08-af2c-4ec6-966c-ed97362704",
    }
    mock_users.called == True
    response = client.get('/users/' + result['id'], headers=headers_)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    else:
        assert response.status_code == 422
        assert response.json() == {
            'detail': [{
                'loc': ['path', 'user_id'],
                'msg': 'value is not a valid uuid',
                'type': 'type_error.uuid'
            }]
        }


def test_not_exist_user(client, mocker: MockFixture):
    mock_users = mocker.patch('controller.users.users')
    result = mock_users.return_value.select.return_value.select_from.return_value.where.return_value.execute.return_value.fetchall.return_value = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    }
    mock_users.called == True
    response = client.get('/users/' + result['id'], headers=headers_)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    else:
        assert response.status_code == 404
        assert response.json() == {'message': 'Not Exist'}


def test_post_user(client, mocker: MockFixture):
    mock_users = mocker.patch('controller.users.users')
    result = mock_users.return_value.insert.return_value.values.return_value.execute.return_value.first.return_value = {
        "first_name": "osama10",
        "last_name": "osama10",
        "email": "osama@hotmail.com",
        "address_id": "f995157d-bd65-4f91-a6fc-5649535f0645",
        "password": "123456789"
    }
    mock_users.called == True
    response = client.post('/users/', json=result)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    elif response.status_code == 400:
        assert response.status_code == 400
        assert response.json()['message'] == 'violates constraint'
    else:
        assert response.status_code == 201
        assert response.json()['email'] == result['email']


def test_post_user_with_missing_value(client, mocker: MockFixture):
    mock_users = mocker.patch('controller.users.users')
    result = mock_users.return_value.insert.return_value.values.return_value.execute.return_value.first.return_value = {
        "last_name": "osama10",
        "email": "osama@hotmail.com",
        "address_id": "f995157d-bd65-4f91-a6fc-5649535f0645",
        "password": "123456789"
    }
    mock_users.called == True
    response = client.post('/users/', json=result)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    else:
        assert response.status_code == 422
        assert response.json() == {
            'detail': [{
                'loc': ['body', 'first_name'],
                'msg': 'field required',
                'type': 'value_error.missing'
            }]
        }


def test_post_user_violate(client, mocker: MockFixture):
    mock_users = mocker.patch('controller.users.users')
    result = mock_users.return_value.insert.return_value.values.return_value.execute.return_value.first.return_value = {
        "first_name": "os",
        "last_name": "osama10",
        "email": "osama@hotmail.com",
        "address_id": "f995157d-bd65-4f91-a6fc-5649535f0645",
        "password": "123456789"
    }
    mock_users.called == True
    response = client.post('/users/', json=result)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    else:
        assert response.status_code == 422
        assert response.json() == {
            'detail': [{
                'ctx': {
                    'pattern': '[A-Za-z]{5,50}'
                },
                'loc': ['body', 'first_name'],
                'msg': 'string does not match regex "[A-Za-z]{5,50}"',
                'type': 'value_error.str.regex'
            }]
        }


def test_delete_user(client, mocker: MockFixture):
    mock_users = mocker.patch('controller.users.users')
    result = mock_users.return_value.delete.return_value.values.return_value.execute.return_value.first.return_value = {
        "id": "2492597e-bfae-4708-9dab-a1aabee2ea27",
        "first_name": "osama10",
        "last_name": "osama10",
        "email": "osama@hotmail.com",
        "created_at": "2021-07-15T14:38:45.814211",
        "updated_at": "2021-07-15T14:38:45.814216",
        "address": {
            "id": "f995157d-bd65-4f91-a6fc-5649535f0645",
            "name": "Aqaba55",
            "zip_code": "10236",
            "building_number": 10,
            "street_name": "putmainstreet",
            "created_at": "2021-07-11T09:59:59.339717",
            "updated_at": "2021-07-14T10:12:15.032628"
        }
    }
    mock_users.called == True
    response = client.delete('/users/' + result['id'], headers=headers_)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    elif response.status_code == 404:
        assert response.status_code == 404
        assert response.json() == {'message': 'Not Exist'}
    else:
        assert response.status_code == 204
        assert response.json()['first_name'] == result['first_name']


def test_delete_user_wrong_id(client, mocker: MockFixture):
    mock_users = mocker.patch('controller.users.users')
    result = mock_users.return_value.delete.return_value.values.return_value.execute.return_value.first.return_value = {
        "id": "2492597e-bfae-4708-9dab-a1aabee2ea",
    }
    mock_users.called == True
    response = client.delete('/users/' + result['id'], headers=headers_)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    else:
        assert response.status_code == 422
        assert response.json() == {
            'detail': [{
                'loc': ['path', 'user_id'],
                'msg': 'value is not a valid uuid',
                'type': 'type_error.uuid'
            }]
        }


def test_delete_user_not_exist(client, mocker: MockFixture):
    mock_users = mocker.patch('controller.users.users')
    result = mock_users.return_value.delete.return_value.values.return_value.execute.return_value.first.return_value = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    }
    mock_users.called == True
    response = client.delete('/users/' + result['id'], headers=headers_)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    else:
        assert response.status_code == 404
        assert response.json() == {'message': 'Not Exist'}


def test_put_user(client, mocker: MockFixture):
    mock_users = mocker.patch('controller.users.users')
    result = mock_users.return_value.update.return_value.select_from.return_value.where.return_value.execute.return_value.fetchall.return_value = {
        "id": "1fe4ab08-af2c-4ec6-966c-ed9736270b4c",
        "first_name": "ahmad10",
        "last_name": "ahmad10",
        "email": "ah10@hotmail.com",
        "address_id": "a3d1918d-9420-451f-9d25-1f9313d7891c",
        "password": "123456789"
    }
    mock_users.called == True
    response = client.put('/users/' + result['id'],
                          headers=headers_,
                          json=result)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    elif response.status_code == 400:
        assert response.status_code == 400
        assert response.json()['message'] == 'violates constraint'
    elif response.status_code == 404:
        assert response.status_code == 404
        assert response.json() == {'message': 'Not Exist'}
    else:
        assert response.status_code == 201
        assert response.json()['first_name'] == result['first_name']


def test_put_user_missing_value(client, mocker: MockFixture):
    mock_users = mocker.patch('controller.users.users')
    result = mock_users.return_value.update.return_value.select_from.return_value.where.return_value.execute.return_value.fetchall.return_value = {
        "id": "1fe4ab08-af2c-4ec6-966c-ed9736270b4c",
        "last_name": "ahmad10",
        "email": "ah10@hotmail.com",
        "address_id": "a3d1918d-9420-451f-9d25-1f9313d7891c",
        "password": "123456789"
    }
    mock_users.called == True
    response = client.put('/users/' + result['id'],
                          headers=headers_,
                          json=result)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    elif response.status_code == 400:
        assert response.status_code == 400
        assert response.json()['message'] == 'violates constraint'
    else:
        assert response.status_code == 422
        assert response.json() == {
            'detail': [{
                'loc': ['body', 'first_name'],
                'msg': 'field required',
                'type': 'value_error.missing'
            }]
        }


def test_put_user_violate(client, mocker: MockFixture):
    mock_users = mocker.patch('controller.users.users')
    result = mock_users.return_value.update.return_value.select_from.return_value.where.return_value.execute.return_value.fetchall.return_value = {
        "id": "1fe4ab08-af2c-4ec6-966c-ed9736270b4c",
        "last_name": "ahmad10",
        "email": "ah10@hotmail.com",
        "address_id": "a3d1918d-9420-451f-9d25-1f9313d7891c",
        "password": "123456789"
    }
    mock_users.called == True
    response = client.put('/users/' + result['id'],
                          headers=headers_,
                          json=result)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    elif response.status_code == 400:
        assert response.status_code == 400
        assert response.json()['message'] == 'violates constraint'
    else:
        assert response.status_code == 422
        assert response.json() == {
            'detail': [{
                'loc': ['body', 'first_name'],
                'msg': 'field required',
                'type': 'value_error.missing'
            }]
        }
