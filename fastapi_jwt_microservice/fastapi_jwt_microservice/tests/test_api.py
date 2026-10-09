import os
from pathlib import Path

TEST_DB = Path("test_app.db")
if TEST_DB.exists():
    TEST_DB.unlink()

os.environ["DATABASE_URL"] = "sqlite:///./test_app.db"
os.environ["SECRET_KEY"] = "test-secret-key"

from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def teardown_module():
    Base.metadata.drop_all(bind=engine)
    if TEST_DB.exists():
        TEST_DB.unlink()


def test_root_and_health():
    assert client.get("/").status_code == 200
    assert client.get("/health").json()["status"] == "healthy"


def test_register_and_login():
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass123",
        },
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    assert "hashed_password" not in response.json()

    duplicate = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "other@example.com",
            "password": "StrongPass123",
        },
    )
    assert duplicate.status_code == 409

    login = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "StrongPass123",
        },
    )
    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"
    assert login.json()["access_token"]


def test_invalid_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "WrongPassword123",
        },
    )
    assert response.status_code == 401


def get_token():
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "StrongPass123",
        },
    )
    return response.json()["access_token"]


def test_protected_crud():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    unauthorized = client.get("/items/")
    assert unauthorized.status_code == 401

    created = client.post(
        "/items/",
        headers=headers,
        json={
            "title": "My first item",
            "description": "Protected CRUD test",
        },
    )
    assert created.status_code == 201
    item_id = created.json()["id"]

    listed = client.get("/items/", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    fetched = client.get(f"/items/{item_id}", headers=headers)
    assert fetched.status_code == 200

    updated = client.put(
        f"/items/{item_id}",
        headers=headers,
        json={"title": "Updated item"},
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Updated item"

    deleted = client.delete(
        f"/items/{item_id}",
        headers=headers,
    )
    assert deleted.status_code == 204

    missing = client.get(f"/items/{item_id}", headers=headers)
    assert missing.status_code == 404


def test_validation():
    response = client.post(
        "/auth/register",
        json={
            "username": "x",
            "email": "not-an-email",
            "password": "123",
        },
    )
    assert response.status_code == 422


def test_me():
    token = get_token()
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
