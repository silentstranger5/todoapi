from .database_config import client, test_db


def get_token():
    response = client.post(
        "/auth/token",
        json={"username": "user", "password": "password"},
    )
    data = response.json()
    return data["access_token"]


def get_guest_token():
    response = client.post(
        "/auth/token",
        json={"username": "guest", "password": "password"},
    )
    data = response.json()
    return data["access_token"]


def test_get_tasks(test_db):
    token = get_token()
    response = client.get(
        "/tasks/get",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tasks"] == []


def test_get_tasks_no_token(test_db):
    response = client.get("/tasks/get")
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Not authorized"


def test_get_tasks_invalid_header(test_db):
    response = client.get(
        "/tasks/get",
        headers={"Authorization": "Invalid"}
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Invalid Authorization header format"
    response = client.get(
        "/tasks/get",
        headers={"Authorization": "Bearer Nonexistent"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Not authorized"


def test_get_tasks_no_access(test_db):
    token = get_guest_token()
    response = client.get(
        "/tasks/get",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tasks"] == []


def test_create_task(test_db):
    token = get_token()
    response = client.post(
        "/tasks/create",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Write an application"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task successfully created"


def test_get_created_task(test_db):
    token = get_token()
    response = client.get(
        "/tasks/get",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tasks"] == [
        {"id": 1, "name": "Write an application", "complete": False, "author_id": 1}
    ]


def test_update_task(test_db):
    token = get_token()
    response = client.post(
        "/tasks/update",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": 1, "name": "Wash the dishes", "complete": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task successfully updated"
    response = client.get(
        "/tasks/get",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tasks"] == [
        {"id": 1, "name": "Wash the dishes", "complete": True, "author_id": 1}
    ]


def test_update_task_invalid_id(test_db):
    token = get_token()
    response = client.post(
        "/tasks/update",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": 5, "name": "Debug an old project"},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Task does not exist"


def test_update_task_no_access(test_db):
    token = get_guest_token()
    response = client.post(
        "/tasks/update",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": 1, "name": "Write tests", "complete": True},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "You don't have permission to update this task"


def test_task_delete(test_db):
    token = get_token()
    response = client.post(
        "/tasks/delete",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task successfully deleted"
