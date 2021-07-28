from http import HTTPStatus
from flask import json
from flask.testing import FlaskClient
from sqlalchemy.orm import joinedload
from main import jwt


def register(client: FlaskClient, username, password):
    return client.post('/users', json=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def get(client: FlaskClient, user_id):
    return client.get(f'/users/{user_id}')


def delete(client: FlaskClient, user_id):
    return client.delete(f'/users/{user_id}')


def update(client: FlaskClient, id, user):
    return client.put(f'/users/{id}', json=user)


def get_user_id_from_data(data):
    auth_token = data["auth_token"]
    payload = jwt.decode(auth_token)
    user_id = payload.user_id
    return user_id


def test_registration(client: FlaskClient):
    res = register(client, 'test', 'test')

    assert b'auth_token' in res.data
    user_id = get_user_id_from_data(json.loads(res.data))
    assert user_id is not None

    user = get(client, user_id)
    user = json.loads(user.data)
    user['deposit'] = 100
    update(client, user_id, user)
    user = get(client, user_id)
    user = json.loads(user.data)

    assert user['deposit'] == 100
    delete(client, user_id)


def test_update_user_not_valid(client: FlaskClient):
    res = update(client, -1, {})
    assert res.status_code == HTTPStatus.NOT_FOUND


def test_delete_user_doesnt_exist(client: FlaskClient):
    res = delete(client, -1)
    assert res.status_code == HTTPStatus.NOT_FOUND
