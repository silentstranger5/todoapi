from .database_config import client, test_db


def test_create_user(test_db):
    response = client.post(
        "/auth/register",
        json={"username": "user", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Registration is successful"


def test_another_user(test_db):
    response = client.post(
        "/auth/register",
        json={"username": "guest", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Registration is successful"


def test_create_same_user(test_db):
    response = client.post(
        "/auth/register",
        json={"username": "user", "password": "password"},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "User already exists"


def test_create_user_no_username(test_db):
    response = client.post(
        "/auth/register",
        json={"password": "password"},
    )
    assert response.status_code == 422
    data = response.json()
    assert 'username' in data['detail'][0]['loc']
    assert data['detail'][0]['msg'] == "Field required"
    assert data['detail'][0]['type'] == "missing"


def test_create_user_no_password(test_db):
    response = client.post(
        "/auth/register",
        json={"username": "user"},
    )
    assert response.status_code == 422
    data = response.json()
    assert 'password' in data['detail'][0]['loc']
    assert data['detail'][0]['msg'] == "Field required"
    assert data['detail'][0]['type'] == "missing"


def test_get_user_token(test_db):
    response = client.post(
        "/auth/token",
        json={"username": "user", "password": "password"},
    )
    assert response.status_code == 200


def test_get_user_token_no_username(test_db):
    response = client.post(
        "/auth/token",
        json={"password": "password"},
    )
    assert response.status_code == 422
    data = response.json()
    assert 'username' in data['detail'][0]['loc']
    assert data['detail'][0]['msg'] == "Field required"
    assert data['detail'][0]['type'] == "missing"


def test_get_user_token_no_password(test_db):
    response = client.post(
        "/auth/token",
        json={"username": "user"},
    )
    assert response.status_code == 422
    data = response.json()
    assert 'password' in data['detail'][0]['loc']
    assert data['detail'][0]['msg'] == "Field required"
    assert data['detail'][0]['type'] == "missing"


def test_get_user_token_invalid_username(test_db):
    response = client.post(
        "/auth/token",
        json={"username": "wrong", "password": "password"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Incorrect user name or password"}


def test_get_user_token_invalid_password(test_db):
    response = client.post(
        "/auth/token",
        json={"username": "user", "password": "wrong"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Incorrect user name or password"}
