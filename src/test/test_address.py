from pytest_mock import MockFixture

headers_ = {
    'Authorization':
    'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvc0Bob3RtYWlsLmNvbSIsImV4cCI6MTYyNzU0Nzg0OH0.USBN7YFOapTDucQKNAk4guS3IXnYiCapmhi_Jyyn5U0'
}


def test_get_addresses(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.select')
    mock_address.return_value.execute.return_value.fetchall.return_value = []

    response = client.get('/address/', headers=headers_)
    assert response.status_code == 404


def test_get_addresses_not_found(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.select')
    mock_address.return_value.execute.return_value.first.return_value = [{
        "id":
        "29309b48-fff3-4b77-b07b-c4006e899fc1",
        "name":
        "Amman",
        "zip_code":
        "11111",
        "building_number":
        5,
        "street_name":
        "mainstretamman",
        "created_at":
        "2021-07-21T18:35:57.928243",
        "updated_at":
        "2021-07-21T18:35:57.928250"
    }]
    response = client.get('/address/', headers=headers_)
    assert response.status_code == 200


def test_unauthorized(client):
    response = client.get('/address/')
    assert response.status_code == 401
    assert response.json() == {'message': 'Not UNAUTHORIZED'}


def test_get_address_by_id(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.select')
    mock_address.return_value.where.return_value.execute.return_value.first.return_value = {
        "id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
        "name": "Amman",
        "zip_code": "11111",
        "building_number": 5,
        "street_name": "mainstretamman",
        "created_at": "2021-07-21T18:35:57.928243",
        "updated_at": "2021-07-21T18:35:57.928250"
    }

    response = client.get('/address/29309b48-fff3-4b77-b07b-c4006e899fc1',
                          headers=headers_)
    assert response.status_code == 200


def test_get_empty_address_by_id(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.select')
    mock_address.return_value.where.return_value.execute.return_value.first.return_value = {}

    response = client.get('/address/29309b48-fff3-4b77-b07b-c4006e899f55',
                          headers=headers_)
    assert response.status_code == 404


def test_post(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.insert')
    mock_address.return_value.values.return_value.returning.return_value.\
        execute.return_value.first.return_value = {
            "id": "5796d483-8a28-48b0-b288-fda6454041b5",
            "name": "Irbid",
            "zip_code": "25252",
            "building_number": 7,
            "street_name": "mainstreet",
            "created_at": "2021-07-25T07:43:03.015999",
            "updated_at": "2021-07-25T07:43:03.016005"
        }
    result = {
        "name": "Irbid",
        "zip_code": "25252",
        "building_number": 7,
        "street_name": "mainstreet",
    }
    response = client.post('/address/', headers=headers_, json=result)
    assert response.status_code == 201


def test_post_missing_value_address(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.insert')
    mock_address.return_value.values.return_value.returning.return_value.\
        execute.return_value.first.return_value = {
            "zip_code": "25252",
            "building_number": 7,
            "street_name": "mainstreet"
        }
    result = {"name": "Irbid", "zip_code": "25252", "building_number": 7}
    response = client.post('/address/', headers=headers_, json=result)
    assert response.status_code == 400


def test_post_empty_return(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.insert')
    mock_address.return_value.values.return_value.returning.return_value.\
        execute.return_value.first.return_value = {}
    result = {
        "name": "Irbid",
        "zip_code": "25252",
        "building_number": 7,
        "street_name": "mainstreet",
    }
    response = client.post('/address/', headers=headers_, json=result)
    assert response.status_code == 404


def test_delete(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.select')
    mock_address.return_value.where.return_value.execute.return_value.first.return_value = {
        "id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
        "name": "Amman",
        "zip_code": "11111",
        "building_number": 5,
        "street_name": "mainstretamman",
        "created_at": "2021-07-21T18:35:57.928243",
        "updated_at": "2021-07-21T18:35:57.928250"
    }

    response = client.get('/address/29309b48-fff3-4b77-b07b-c4006e899fc1',
                          headers=headers_)
    if response.status_code == 200:
        mock_address = mocker.patch(
            'controllers.address_controllers.address.delete')
        mock_address.return_value.where.return_value.returning.return_value.\
            execute.return_value.first.return_value = {
                "id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
                "name": "Amman",
                "zip_code": "11111",
                "building_number": 5,
                "street_name": "mainstretamman",
                "created_at": "2021-07-21T18:35:57.928243",
                "updated_at": "2021-07-21T18:35:57.928250"
            }
        response = client.delete(
            '/address/29309b48-fff3-4b77-b07b-c4006e899fc1', headers=headers_)
        assert response.status_code == 204


def test_delete_address_wrong_id(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.select')
    mock_address.return_value.where.return_value.execute.return_value.first.return_value = {
        "id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
        "name": "Amman",
        "zip_code": "11111",
        "building_number": 5,
        "street_name": "mainstretamman",
        "created_at": "2021-07-21T18:35:57.928243",
        "updated_at": "2021-07-21T18:35:57.928250"
    }

    response = client.get('/address/29309b48-fff3-4b77-b07b-c4006e899f45',
                          headers=headers_)
    if response.status_code == 404:
        mock_address = mocker.patch(
            'controllers.address_controllers.address.delete')
        mock_address.return_value.where.return_value.returning.return_value.\
            execute.return_value.first.return_value = {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "string",
                "zip_code": "string",
                "building_number": 0,
                "street_name": "string",
            }
        response = client.delete(
            '/address/3fa85f64-5717-4562-b3fc-2c963f66af45', headers=headers_)
        assert response.status_code == 404


def test_delete_error(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.select')
    mock_address.return_value.where.return_value.execute.return_value.first.return_value = {}

    response = client.get('/address/29309b48-fff3-4b77-b07b-c4006e899f45',
                          headers=headers_)
    if response.status_code == 404:
        mock_address = mocker.patch(
            'controllers.address_controllers.address.delete')
        mock_address.return_value.where.return_value.returning.return_value.\
            execute.return_value.first.return_value = {}
        response = client.delete(
            '/address/5796d483-8a28-48b0-b288-fda6454041b5', headers=headers_)
        assert response.status_code == 404


def test_put(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.select')
    mock_address.return_value.where.return_value.execute.return_value.first.return_value = {
        "id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
        "name": "Amman",
        "zip_code": "11111",
        "building_number": 5,
        "street_name": "mainstretamman",
        "created_at": "2021-07-21T18:35:57.928243",
        "updated_at": "2021-07-21T18:35:57.928250"
    }

    response = client.get('/address/29309b48-fff3-4b77-b07b-c4006e899fc1',
                          headers=headers_)
    if response.status_code == 200:
        mock_address = mocker.patch(
            'controllers.address_controllers.address.update')
        mock_address.return_value.where.return_value.values.return_value.returning.return_value.\
            execute.return_value.first.return_value = {
                "id": "5796d483-8a28-48b0-b288-fda6454041b5",
                "name": "Petra",
                "zip_code": "25252",
                "building_number": 7,
                "street_name": "mainstreet",
                "created_at": "2021-07-25T07:43:03.015999",
                "updated_at": "2021-07-25T07:43:03.016005"
            }
        result = {
            "name": "Petra",
            "zip_code": "25252",
            "building_number": 7,
            "street_name": "mainstreet",
        }
        response = client.put('/address/5796d483-8a28-48b0-b288-fda6454041b5',
                              headers=headers_,
                              json=result)
        assert response.status_code == 201


def test_put_not_exist(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.select')
    mock_address.return_value.where.return_value.execute.return_value.first.return_value = {
        "id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
        "name": "Amman",
        "zip_code": "11111",
        "building_number": 5,
        "street_name": "mainstretamman",
        "created_at": "2021-07-21T18:35:57.928243",
        "updated_at": "2021-07-21T18:35:57.928250"
    }

    response = client.get('/address/29309b48-fff3-4b77-b07b-c4006e899f45',
                          headers=headers_)
    if response.status_code == 404:
        mock_address = mocker.patch(
            'controllers.address_controllers.address.update')
        mock_address.return_value.where.return_value.values.return_value.returning.return_value.\
            execute.return_value.first.return_value = {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "teststring",
                "zip_code": "12563",
                "building_number": 0,
                "street_name": "teststring",
            }
        result = {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "name": "teststring",
            "zip_code": "12563",
            "building_number": 0,
            "street_name": "teststring",
        }
        response = client.put('/address/3fa85f64-5717-4562-b3fc-2c963f66afa6',
                              headers=headers_,
                              json=result)
        assert response.status_code == 404


def test_violate_put(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.update')
    mock_address.return_value.where.return_value.values.return_value.returning.return_value.\
        execute.return_value.first.return_value = {
            "id": "5796d483-8a28-48b0-b288-fda6454041b5",
            "name": "Petra",
            "zip_code": "25252",
            "building_number": 7,
            "street_name": "mainstreet",
            "created_at": "2021-07-25T07:43:03.015999",
            "updated_at": "2021-07-25T07:43:03.016005"
        }
    result = {
        "name": "Petra",
        "zip_code": "25",
        "building_number": 7,
        "street_name": "mainstreet",
    }
    response = client.put('/address/5796d483-8a28-48b0-b288-fda6454041b5',
                          headers=headers_,
                          json=result)
    assert response.status_code == 422


def test_put_404(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.select')
    mock_address.return_value.where.return_value.execute.return_value.first.return_value = {}
    response = client.get('/address/29309b48-fff3-4b77-b07b-c4006e899f45',
                          headers=headers_)
    if response.status_code == 404:
        mock_address = mocker.patch(
            'controllers.address_controllers.address.update')
        mock_address.return_value.where.return_value.values.return_value.returning.return_value.\
            execute.return_value.first.return_value = {}
        result = {
            "name": "Petra",
            "zip_code": "25548",
            "building_number": 7,
            "street_name": "mainstreet",
        }
        response = client.put('/address/5796d483-8a28-48b0-b288-fda6454041b5',
                              headers=headers_,
                              json=result)
        assert response.status_code == 404


def test_patch(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.select')
    mock_address.return_value.where.return_value.execute.return_value.first.return_value = {
        "id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
        "name": "Amman",
        "zip_code": "11111",
        "building_number": 5,
        "street_name": "mainstretamman",
        "created_at": "2021-07-21T18:35:57.928243",
        "updated_at": "2021-07-21T18:35:57.928250"
    }

    response = client.get('/address/29309b48-fff3-4b77-b07b-c4006e899fc1',
                          headers=headers_)
    if response.status_code == 200:
        mock_address = mocker.patch(
            'controllers.address_controllers.address.update')
        mock_address.return_value.where.return_value.values.return_value.returning.return_value.\
            execute.return_value.first.return_value = {
                "id": "5796d483-8a28-48b0-b288-fda6454041b5",
                "name": "Petra",
                "zip_code": "25252",
                "building_number": 7,
                "street_name": "mainstreet",
                "created_at": "2021-07-25T07:43:03.015999",
                "updated_at": "2021-07-25T07:43:03.016005"
            }
        result = {
            "name": "Petra",
            "zip_code": "25252",
            "building_number": 7,
            "street_name": "mainstreet",
        }
        response = client.patch(
            '/address/5796d483-8a28-48b0-b288-fda6454041b5',
            headers=headers_,
            json=result)
        assert response.status_code == 201


def test_patch_not_exist(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.select')
    mock_address.return_value.where.return_value.execute.return_value.first.return_value = {
        "id": "29309b48-fff3-4b77-b07b-c4006e899fc1",
        "name": "Amman",
        "zip_code": "11111",
        "building_number": 5,
        "street_name": "mainstretamman",
        "created_at": "2021-07-21T18:35:57.928243",
        "updated_at": "2021-07-21T18:35:57.928250"
    }

    response = client.get('/address/29309b48-fff3-4b77-b07b-c4006e899f45',
                          headers=headers_)
    if response.status_code == 404:
        mock_address = mocker.patch(
            'controllers.address_controllers.address.update')
        mock_address.return_value.where.return_value.values.return_value.returning.return_value.\
            execute.return_value.first.return_value = {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "teststring",
                "zip_code": "12563",
                "building_number": 0,
                "street_name": "teststring",
            }
        result = {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "name": "teststring",
            "zip_code": "12563",
            "building_number": 0,
            "street_name": "teststring",
        }
        response = client.patch('/address/3fa85f64-5717-4562-b3fc-2c963f66afa6',
                                headers=headers_,
                                json=result)
        assert response.status_code == 404


def test_violate_patch(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.update')
    mock_address.return_value.where.return_value.values.return_value.returning.return_value.\
        execute.return_value.first.return_value = {

            "id": "5796d483-8a28-48b0-b288-fda6454041b5",
            "name": "Petra",
            "zip_code": "25252",
            "building_number": 7,
            "street_name": "mainstreet",
            "created_at": "2021-07-25T07:43:03.015999",
            "updated_at": "2021-07-25T07:43:03.016005"
        }
    result = {
        "name": "Petra",
        "zip_code": "25",
        "building_number": 7,
        "street_name": "mainstreet",
    }
    response = client.patch('/address/5796d483-8a28-48b0-b288-fda6454041b5',
                            headers=headers_,
                            json=result)
    assert response.status_code == 422


def test_patch_404(client, mocker: MockFixture):
    mock_address = mocker.patch(
        'controllers.address_controllers.address.select')
    mock_address.return_value.where.return_value.execute.return_value.first.return_value = {}
    response = client.get('/address/29309b48-fff3-4b77-b07b-c4006e899f45',
                          headers=headers_)
    if response.status_code == 404:
        mock_address = mocker.patch(
            'controllers.address_controllers.address.update')
        mock_address.return_value.where.return_value.values.return_value.returning.return_value.\
            execute.return_value.first.return_value = {}
        result = {
            "name": "Petra",
            "zip_code": "25458",
            "building_number": 7,
            "street_name": "mainstreet",
        }
        response = client.patch('/address/5796d483-8a28-48b0-b288-fda6454041b5',
                                headers=headers_,
                                json=result)
        assert response.status_code == 404
