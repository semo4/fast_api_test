from pytest_mock import MockFixture

headers_ = {
    'Authorization':
    'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvc0Bob3RtYWlsLmNvbSIsImV4cCI6MTYyNjM2MzQ3Mn0.rwbX1NXzqz5vNYS6EE7HU4CXkvyhUv7jRfNTjGt02so'
}


def test_get_addresses(client, mocker: MockFixture):
    mock_address = mocker.patch('controller.address.address')
    result = mock_address.return_value.select.return_value.execute.return_value.fetchall.return_value.called = {
        'name': 'Amman'
    }
    mock_address.called == True
    response = client.get('/address/', headers=headers_)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    else:
        assert response.status_code == 200
        assert response.json()[0]['name'] == result['name']


def test_unauthorized(client):
    response = client.get('/address/')
    assert response.status_code == 401
    assert response.json() == {'message': 'Not UNAUTHORIZED'}


def test_get_address_by_id(client, mocker: MockFixture):
    mock_address = mocker.patch('controller.address.address')
    result = mock_address.return_value.select.return_value.execute.return_value.first.return_value = {
        "id": "a3d1918d-9420-451f-9d25-1f9313d7891c",
        "name": "Amman",
        "zip_code": "77777",
        "building_number": 41,
        "street_name": "fbwtbwrtbgfgbtrbA",
        "created_at": "2021-07-12T07:11:57.908966",
        "updated_at": "2021-07-12T07:11:57.908974"
    }
    mock_address.called == True
    response = client.get('/address/' + result['id'], headers=headers_)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    else:
        assert response.status_code == 200
        assert response.json()['name'] == result['name']


def test_single_address_with_wrong_id(client, mocker: MockFixture):
    mock_address = mocker.patch('controller.address.address')
    result = mock_address.return_value.select.return_value.execute.return_value.fetchone.return_value = {
        "id": "a3d1918d-9420-451f-9d25-1f9313d789"
    }
    mock_address.called == True
    response = client.get('/address/' + result['id'], headers=headers_)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    else:
        assert response.status_code == 422
        assert response.json() == {
            'detail': [{
                'loc': ['path', 'address_id'],
                'msg': 'value is not a valid uuid',
                'type': 'type_error.uuid'
            }]
        }


def test_not_found_address(client, mocker: MockFixture):
    mock_address = mocker.patch('controller.address.address')
    result = mock_address.return_value.select.return_value.execute.return_value.first.return_value = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "LosAnglos",
        "zip_code": "74521",
        "building_number": 20,
        "street_name": "Backlongroad",
    }
    mock_address.called == True
    response = client.get('/address/' + result['id'], headers=headers_)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    else:
        assert response.status_code == 404
        assert response.json() == {'message': 'Not Exist'}


def test_post(client, mocker: MockFixture):
    mock_address = mocker.patch('controller.address.address')
    result = mock_address.return_value.insert.return_value.values.return_value.execute.return_value.first.return_value = {
        "name": "Aqaba",
        "zip_code": "45696",
        "building_number": 7,
        "street_name": "mainstreet",
    }
    mock_address.called == True
    response = client.post('/address/', headers=headers_, json=result)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    elif response.status_code == 400:
        assert response.status_code == 400
        assert response.json()['message'] == 'violates constraint'
    else:
        assert response.status_code == 201
        assert response.json()['name'] == result['name']


def test_post_missing_value_address(client, mocker: MockFixture):
    mock_address = mocker.patch('controller.address.address')
    result = mock_address.return_value.insert.return_value.values.return_value.execute.return_value.first.return_value = {
        "zip_code": "74852",
        "building_number": "71",
        "street_name": "armystreet"
    }
    mock_address.called == True
    response = client.post('/address/', headers=headers_, json=result)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    else:
        assert response.status_code == 422
        assert response.json() == {
            'detail': [{
                'loc': ['body', 'name'],
                'msg': 'field required',
                'type': 'value_error.missing'
            }]
        }


def test_post_violate_data(client, mocker: MockFixture):
    mock_address = mocker.patch('controller.address.address')
    result = mock_address.return_value.insert.return_value.values.return_value.execute.return_value.first.return_value = {
        "name": "Zarqa",
        "zip_code": "5",
        "building_number": "71",
        "street_name": "armystreet"
    }
    mock_address.called == True
    response = client.post('/address/', headers=headers_, json=result)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    else:
        assert response.status_code == 422
        assert response.json() == {
            'detail': [{
                'ctx': {
                    'pattern': '[0-9]{5}'
                },
                'loc': ['body', 'zip_code'],
                'msg': 'string does not match regex "[0-9]{5}"',
                'type': 'value_error.str.regex'
            }]
        }


def test_delete_foreign_key(client, mocker: MockFixture):

    mock_address = mocker.patch('controller.address.address')
    result = mock_address.return_value.select.return_value.values.return_value.execute.return_value.first.return_value = {
        "id": "a3d1918d-9420-451f-9d25-1f9313d7891c",
        "name": "Amman",
        "zip_code": "77777",
        "building_number": 41,
        "street_name": "fbwtbwrtbgfgbtrbA",
    }
    mock_address.called == True

    response = client.delete('/address/' + result['id'], headers=headers_)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    else:
        assert response.status_code == 400
        assert response.json()['message'] == 'violates constraint'


def test_delete_address_wrong_id(client, mocker: MockFixture):
    mock_address = mocker.patch('controller.address.address')
    result = mock_address.return_value.select.return_value.values.return_value.execute.return_value.first.return_value = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "string",
        "zip_code": "string",
        "building_number": 0,
        "street_name": "string",
    }
    mock_address.called == True
    response = client.delete('/address/' + result['id'], headers=headers_)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    else:
        assert response.status_code == 404
        assert response.json() == {'message': 'Not Exist'}


def test_delete_exist(client, mocker: MockFixture):
    mock_address = mocker.patch('controller.address.address')
    result = mock_address.return_value.select.return_value.values.return_value.execute.return_value.first.return_value = {
        "id": "cc8a3095-30b4-49ce-a738-e3bb3aacf902",
        "name": "Aqaba",
        "zip_code": "45696",
        "building_number": 7,
        "street_name": "mainstreet",
        "created_at": "2021-07-14T10:00:17.287564",
        "updated_at": "2021-07-14T10:00:17.287569"
    }
    mock_address.called == True
    response = client.delete('/address/' + result['id'], headers=headers_)
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
        assert response.status_code == 204
        assert response.json()['name'] == result['name']


def test_put(client, mocker: MockFixture):
    mock_address = mocker.patch('controller.address.address')
    result = mock_address.return_value.update.return_value.values.return_value.execute.return_value.first.return_value = {
        "id": "a2223ef3-bb3f-4bc3-afb7-9512b9766840",
        "name": "Petra",
        "zip_code": "25896",
        "building_number": 8,
        "street_name": "ghrfgvddvskhytgggg",
    }
    mock_address.called == True
    response = client.put('/address/' + result['id'],
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
        assert response.json()['name'] == result['name']


def test_put_not_exist(client, mocker: MockFixture):
    mock_address = mocker.patch('controller.address.address')
    result = mock_address.return_value.update.return_value.values.return_value.execute.return_value.first.return_value = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "teststring",
        "zip_code": "12563",
        "building_number": 0,
        "street_name": "teststring",
    }
    mock_address.called == True
    response = client.put('/address/' + result['id'],
                          headers=headers_,
                          json=result)
    if response.status_code == 401:
        assert response.status_code == 401
        assert response.json() == {'message': 'Not UNAUTHORIZED'}
    elif response.status_code == 400:
        assert response.status_code == 400
        assert response.json()['message'] == 'violates constraint'
    else:
        assert response.status_code == 404
        assert response.json() == {'message': 'Not Exist'}


def test_put_missing_value(client, mocker: MockFixture):
    mock_address = mocker.patch('controller.address.address')
    result = mock_address.return_value.update.return_value.values.return_value.execute.return_value.first.return_value = {
        "id": "a2223ef3-bb3f-4bc3-afb7-9512b9766840",
        "zip_code": "25896",
        "building_number": 8,
        "street_name": "ghrfgvddvskhytgggg",
    }
    mock_address.called == True
    response = client.put('/address/' + result['id'],
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
                'loc': ['body', 'name'],
                'msg': 'field required',
                'type': 'value_error.missing'
            }]
        }


def test_put_violate(client, mocker: MockFixture):
    mock_address = mocker.patch('controller.address.address')
    result = mock_address.return_value.update.return_value.values.return_value.execute.return_value.first.return_value = {
        "id": "a2223ef3-bb3f-4bc3-afb7-9512b9766840",
        "name": "kj",
        "zip_code": "25894",
        "building_number": 8,
        "street_name": "ghrfgvddvskhytgggg",
    }
    mock_address.called == True
    response = client.put('/address/' + result['id'],
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
                'ctx': {
                    'pattern': '[A-Za-z]{5,50}'
                },
                'loc': ['body', 'name'],
                'msg': 'string does not match regex "[A-Za-z]{5,50}"',
                'type': 'value_error.str.regex'
            }]
        }
