from httpx import AsyncClient


async def test_add_one_user(auth_ac: AsyncClient):
    response = await auth_ac.post("/users", json={
        "email": "test@test.com",
        "password": "12345"
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_add_one_user_invalid_email_unique(auth_ac: AsyncClient):
    response = await auth_ac.post("/users", json={
        "email": "test@test.com",
        "password": "12345"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: user.email"


async def test_add_one_user_invalid_name(auth_ac: AsyncClient):
    response = await auth_ac.post("/users", json={
        "first_name": "234",
        "email": "test@test2.com",
        "password": "12345"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for name field"


async def test_add_one_user_invalid_phone(auth_ac: AsyncClient):
    response = await auth_ac.post("/users", json={
        "phone": "asd",
        "email": "test@test2.com",
        "password": "12345"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for phone field"


async def test_get_list_users(auth_ac: AsyncClient):
    response = await auth_ac.get("/users")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2


async def test_get_one_user(auth_ac: AsyncClient):
    response = await auth_ac.get("/users/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_edit_one_user(auth_ac: AsyncClient):
    response = await auth_ac.patch("/users/2", json={
        "first_name": "Test",
        "email": "test@test.com",
        "password": "12345"
    })

    assert response.status_code == 200
    assert response.json()["first_name"] == "Test"
    assert response.json()["id"] == 2


async def test_edit_one_user_invalid_name(auth_ac: AsyncClient):
    response = await auth_ac.patch("/users/2", json={
        "first_name": "123",
        "email": "test@test.com",
        "password": "12345"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for name field"


async def test_delete_one_user(auth_ac: AsyncClient):
    response = await auth_ac.delete("/users/2")

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
