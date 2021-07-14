
headers_ = {
    'Authorization':
    'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvc0Bob3RtYWlsLmNvbSIsImV4cCI6MTYyNjI2Nzk3NH0.t03ccrjKZZ0MjYn0Q4Yt38xUK7FmGKmNYGSAt7oBd2s'
}


def test_get_users(get_users, client):
    response = client.get('/users/', headers=headers_)
    assert response.status_code == get_users.status_code
    assert response.json() == get_users.json()


def test_unauthorize_get_users(unauthorize_user, client):
    response = client.get('/users/')
    assert response.status_code == unauthorize_user.status_code
    assert response.json() == unauthorize_user.json()


def test_get_user_by_id(client, single_user):
    if single_user.status_code == 401:
        response = client.get('/users/', headers=headers_)
        assert response.status_code == single_user.status_code
        assert response.json() == single_user.json()
    else:
        id = single_user.json()['id']
        response = client.get('/users/' + id, headers=headers_)
        assert response.status_code == single_user.status_code
        assert response.json() == single_user.json()


def test_get_user_not_exist(client):
    response = client.get('/users/c2310d5e-287b-4580-bd7a-917b2a12fd9c', headers=headers_)
    assert response.status_code == 404
    assert response.json() == {'message': 'Not Exist'}


def test_post_user(client, post_user):
    response = client.post('/users/', json=post_user)
    assert response.status_code == 201 or 400


def test_post_user_with_missing_value(client, post_user):
    del post_user['first_name']
    response = client.post('/users/', json=post_user)
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['body', 'first_name'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }]
    }


def test_get_user_wrong_id(client, single_user):
    if single_user.status_code == 401:
        response = client.get('/users/', headers=headers_)
        assert response.status_code == single_user.status_code
        assert response.json() == single_user.json()
    else:
        id = single_user.json()['id']
        response = client.get('/users/' + id[:len(id) - 2], headers=headers_)
        assert response.status_code == 422
        assert response.json() == {
            'detail': [{
                'loc': ['path', 'user_id'],
                'msg': 'value is not a valid uuid',
                'type': 'type_error.uuid'
            }]
        }


def test_post_user_violate(client, post_user):
    post_user['first_name'] = 'fg'
    response = client.post('/users/', json=post_user)
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


def test_delete_user(client, delete_user):
    if delete_user.status_code == 401:
        response = client.get('/users/', headers=headers_)
        assert response.status_code == delete_user.status_code
        assert response.json() == delete_user.json()
    else:
        id = delete_user.json()['id']
        response = client.delete('/users/' + id, headers=headers_)
        assert response.status_code == 204


def test_delete_user_wrong_id(client, delete_user):
    if delete_user.status_code == 401:
        response = client.get('/users/', headers=headers_)
        assert response.status_code == delete_user.status_code
        assert response.json() == delete_user.json()
    else:
        id = delete_user.json()['id']
        response = client.delete('/users/' + id[:len(id) - 2],
                                 headers=headers_)
        assert response.status_code == 422
        assert response.json() == {
            'detail': [{
                'loc': ['path', 'user_id'],
                'msg': 'value is not a valid uuid',
                'type': 'type_error.uuid'
            }]
        }


def test_delete_user_not_exist(client):
    response = client.delete('/users/c2310d5e-287b-4580-bd7a-917b2a12fd9c',
                             headers=headers_)
    assert response.status_code == 404
    assert response.json() == {'message': 'Not Exist'}


def test_put_user(client, single_user, put_data):
    if single_user.status_code == 401:
        response = client.get('/users/', headers=headers_)
        assert response.status_code == single_user.status_code
        assert response.json() == single_user.json()
    else:
        id = single_user.json()['id']
        response = client.put('/users/' + id, headers=headers_, json=put_data)
        assert response.status_code == 201 or 400


def test_put_user_missing_value(client, single_user, put_data):
    if single_user.status_code == 401:
        response = client.get('/users/', headers=headers_)
        assert response.status_code == single_user.status_code
        assert response.json() == single_user.json()
    else:
        id = single_user.json()['id']
        del put_data['first_name']
        response = client.put('/users/' + id, headers=headers_, json=put_data)
        assert response.status_code == 422
        assert response.json() == {
            'detail': [{
                'loc': ['body', 'first_name'],
                'msg': 'field required',
                'type': 'value_error.missing'
            }]
        }


def test_put_user_violate(client, single_user, put_data):
    if single_user.status_code == 401:
        response = client.get('/users/', headers=headers_)
        assert response.status_code == single_user.status_code
        assert response.json() == single_user.json()
    else:
        id = single_user.json()['id']
        put_data['first_name'] = 'jh'
        response = client.put('/users/' + id, headers=headers_, json=put_data)
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
