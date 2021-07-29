from flask.testing import FlaskClient

def login(client: FlaskClient, username, password):
    return client.post(f'/login', json=dict(
        username=username,
        password=password
    ), follow_redirects=True)
