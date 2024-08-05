from .database_config import client, test_db
from .test_tasks import get_token, get_guest_token


def test_create_new_task(test_db):
    token = get_token()
    response = client.post (
        "/tasks/create",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Buy the groceries"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task successfully created"


def test_grant_permission(test_db):
    token = get_token()
    response = client.post(
        "/permissions/grant",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "guest", "task_id": 2},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Permission successfully granted"


def test_grant_permission_invalid_id(test_db):
    token = get_token()
    response = client.post(
        "/permissions/grant",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "guest", "task_id": 5},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Task does not exist or you are not it's author"


def test_grant_permission_no_token(test_db):
    response = client.post(
        "/permissions/grant",
        json={"username": "guest", "task_id": 2},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Not authorized"


def test_grant_permission_invalid_username(test_db):
    token = get_token()
    response = client.post(
        "/permissions/grant",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "invalid", "task_id": 1},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User does not exist"


def test_grant_permission_not_author(test_db):
    token = get_guest_token()
    response = client.post(
        "/permissions/grant",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "user", "task_id": 2},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Task does not exist or you are not it's author"


def test_get_tasks_read_permission(test_db):
    token = get_guest_token()
    response = client.get(
        "/tasks/get",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tasks"] == [
        {"author_id": 1, "complete": False, "id": 2, "name": "Buy the groceries"}
    ]


def test_update_task_no_permission(test_db):
    token = get_guest_token()
    response = client.post(
        "/tasks/update",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": 2, "name": "Throw out trash" },
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "You don't have permission to update this task"


def test_update_task_with_permission(test_db):
    token = get_token()
    response = client.post(
        "/permissions/grant",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "guest", "task_id": 2, "update": True},
    )
    token = get_guest_token()
    response = client.post(
        "/tasks/update",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": 2, "name": "Throw out trash" },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task successfully updated"
    response = client.get(
        "/tasks/get",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tasks"] == [
        {"author_id": 1, "complete": False, "id": 2, "name": "Throw out trash"}
    ]


def test_upgrade_task_boolean_only(test_db):
    token = get_guest_token()
    response = client.post(
        "/tasks/update",
        headers={"Authorization": f"Bearer {token}"},
        json={"id": 2, "complete": True },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task successfully updated"
    response = client.get(
        "/tasks/get",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tasks"] == [
        {"author_id": 1, "complete": True, "id": 2, "name": "Throw out trash"}
    ]


def test_revoke_permission(test_db):
    token = get_token()
    response = client.post(
        "/permissions/revoke",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "guest", "task_id": 2},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Permission successfully revoked"
    token = get_guest_token()
    response = client.get(
        "/tasks/get",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["tasks"] == []
