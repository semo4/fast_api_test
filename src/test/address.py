
headers_ = {
    'Authorization':
    'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvc0Bob3RtYWlsLmNvbSIsImV4cCI6MTYyNjI2Nzk3NH0.t03ccrjKZZ0MjYn0Q4Yt38xUK7FmGKmNYGSAt7oBd2s'
}


def test_get_addresses(client, get_addresses):
    response = client.get('/address/', headers=headers_)
    assert response.status_code == get_addresses.status_code
    assert response.json() == get_addresses.json()


def test_unauthorized(client, unauthorize_address):
    response = client.get('/address/')
    assert response.status_code == unauthorize_address.status_code
    assert response.json() == unauthorize_address.json()


def test_get_address_by_id(client, single_address):
    if single_address.status_code == 401:
        response = client.get('/address/', headers=headers_)
        assert response.status_code == single_address.status_code
        assert response.json() == single_address.json()
    else:
        id = single_address.json()['id']
        response = client.get('/address/' + id, headers=headers_)
        assert response.status_code == single_address.status_code
        assert response.json() == single_address.json()


def test_single_address_with_wrong_id(client, single_address):
    if single_address.status_code == 401:
        response = client.get('/address/', headers=headers_)
        assert response.status_code == single_address.status_code
        assert response.json() == single_address.json()
    else:
        id = single_address.json()['id']
        response = client.get('/address/' + id[:len(id) - 2], headers=headers_)
        assert response.status_code == 422
        assert response.json() == {
            'detail': [{
                'loc': ['path', 'address_id'],
                'msg': 'value is not a valid uuid',
                'type': 'type_error.uuid'
            }]
        }


def test_not_found_address(client):
    response = client.get('/address/3fa85f64-5717-4562-b3fc-2c963f66afa6',
                          headers=headers_)
    assert response.status_code == 404
    assert response.json() == {'message': 'Not Exist'}


def test_post(client, post_address):
    response = client.post('/address/', headers=headers_, json=post_address)
    assert response.status_code == 201 or 400


def test_post_missing_value_address(client, post_address):
    del post_address['zip_code']
    response = client.post('/address/', headers=headers_, json=post_address)
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['body', 'zip_code'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }]
    }


def test_post_violate_data(client, post_address):
    post_address['zip_code'] = '012'
    response = client.post('/address/', headers=headers_, json=post_address)
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


def test_delete_foreign_key(client, single_user):
    id = single_user.json()['address']['id']
    response = client.delete('/address/' + id,
                             headers=headers_)
    assert response.status_code == 400


def test_delete_address_wrong_id(client, single_address):
    if single_address.status_code == 401:
        response = client.get('/address/', headers=headers_)
        assert response.status_code == single_address.status_code
        assert response.json() == single_address.json()
    else:
        id = single_address.json()['id']
        response = client.delete('/address/' + id[:len(id) - 2], headers=headers_)
        assert response.status_code == 422
        assert response.json() == {
            'detail': [{
                'loc': ['path', 'address_id'],
                'msg': 'value is not a valid uuid',
                'type': 'type_error.uuid'
            }]
        }


# def test_delete_exist(client, delete_address):
#     if delete_address.status_code == 401:
#         response = client.get('/address/', headers=headers_)
#         assert response.status_code == delete_address.status_code
#         assert response.json() == delete_address.json()
#     else:
#         id = delete_address.json()['id']
#         response = client.delete('/address/' + id,
#                                 headers=headers_)
#         assert response.status_code == 204
#         assert response.json() == delete_address.json()


def test_delete_not_exist(client):
    response = client.delete('/address/c9a25ab3-1248-4af2-a1fb-be187e9',
                             headers=headers_)
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['path', 'address_id'],
            'msg': 'value is not a valid uuid',
            'type': 'type_error.uuid'
        }]
    }


def test_put(client, single_address, put_address):
    if single_address.status_code == 401:
        response = client.get('/address/', headers=headers_)
        assert response.status_code == single_address.status_code
        assert response.json() == single_address.json()
    else:
        id = single_address.json()['id']
        response = client.put('/address/' + id, headers=headers_, json=put_address)
        assert response.status_code == 201 or 400


def test_put_not_exist(client, put_address):
    response = client.put('/address/3fa85f64-5717-4562-b3fc-2c963f66afa6',
                          headers=headers_,
                          json=put_address)
    assert response.status_code == 404
    assert response.json() == {'message': 'Not Exist'}


def test_put_missing_value(client, single_address, put_address):
    if single_address.status_code == 401:
        response = client.get('/address/', headers=headers_)
        assert response.status_code == single_address.status_code
        assert response.json() == single_address.json()
    else:
        id = single_address.json()['id']
        del put_address['name']
        response = client.put('/address/' + id, headers=headers_, json=put_address)
        assert response.status_code == 422
        assert response.json() == {
            'detail': [{
                'loc': ['body', 'name'],
                'msg': 'field required',
                'type': 'value_error.missing'
            }]
        }


def test_put_violate(client, single_address, put_address):
    if single_address.status_code == 401:
        response = client.get('/address/', headers=headers_)
        assert response.status_code == single_address.status_code
        assert response.json() == single_address.json()
    else:
        id = single_address.json()['id']
        put_address['name'] = 'ff'
        response = client.put('/address/' + id, headers=headers_, json=put_address)
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


# # patch


# def test_patch():
#     put_data['name'] = 'frompatch'
#     response = client.patch('/address/a2223ef3-bb3f-4bc3-afb7-9512b9766840',
#                             headers=headers_,
#                             json=put_data)
#     assert response.status_code == 201


# def test_patch_not_exist():
#     response = client.patch('/address/3fa85f64-5717-4562-b3fc-2c963f66afa6',
#                             headers=headers_,
#                             json=put_data)
#     assert response.status_code == 404
#     assert response.json() == {'message': 'Not Exist'}


# def test_patch_missing():
#     del put_data['zip_code']
#     response = client.patch('/address/a2223ef3-bb3f-4bc3-afb7-9512b9766840',
#                             headers=headers_,
#                             json=put_data)
#     assert response.status_code == 422
#     assert response.json() == {
#         'detail': [{
#             'loc': ['body', 'zip_code'],
#             'msg': 'field required',
#             'type': 'value_error.missing'
#         }]
#     }


# def test_patch_violate():
#     put_data['name'] = 'fdg'
#     put_data['zip_code'] = '45869'
#     response = client.patch('/address/a2223ef3-bb3f-4bc3-afb7-9512b9766840',
#                             headers=headers_,
#                             json=put_data)
#     assert response.status_code == 422
#     assert response.json() == {
#         'detail': [{
#             'ctx': {
#                 'pattern': '[A-Za-z]{5,50}'
#             },
#             'loc': ['body', 'name'],
#             'msg': 'string does not match regex "[A-Za-z]{5,50}"',
#             'type': 'value_error.str.regex'
#         }]
#     }
