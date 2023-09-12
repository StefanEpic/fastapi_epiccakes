from httpx import AsyncClient


async def test_add_one_manager(auth_ac: AsyncClient):
    response = await auth_ac.post("/manufacturer_managers", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+77777777777",
        "email": "boris@test.com",
        "manufacturer_id": 1
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_add_one_manager_invalid_manufacturer(auth_ac: AsyncClient):
    response = await auth_ac.post("/manufacturer_managers", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+77777777777",
        "email": "boris@test.com",
        "manufacturer_id": 55
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Manufacturer with this id not found'


async def test_add_one_manager_invalid_name(auth_ac: AsyncClient):
    response = await auth_ac.post("/manufacturer_managers", json={
        "first_name": "Иван333",
        "second_name": "Иванов",
        "last_name": "Иванович",
        "phone": "+79859859898",
        "email": "ivan@test.com",
        "manufacturer_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for name field"


async def test_add_one_manager_invalid_phone_unique(auth_ac: AsyncClient):
    response = await auth_ac.post("/manufacturer_managers", json={
        "first_name": "Иван",
        "second_name": "Иванов",
        "last_name": "Иванович",
        "phone": "+79859859898",
        "email": "ivan2@test.com",
        "manufacturer_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: manufacturer_manager.phone"


async def test_add_one_manager_invalid_phone_text(auth_ac: AsyncClient):
    response = await auth_ac.post("/manufacturer_managers", json={
        "first_name": "Иван",
        "second_name": "Иванов",
        "last_name": "Иванович",
        "phone": "asd",
        "email": "ivan2@test.com",
        "manufacturer_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for phone field"


async def test_add_one_manager_invalid_email_unique(auth_ac: AsyncClient):
    response = await auth_ac.post("/manufacturer_managers", json={
        "first_name": "Иван",
        "second_name": "Иванов",
        "last_name": "Иванович",
        "phone": "+79839859898",
        "email": "ivan@test.com",
        "manufacturer_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: manufacturer_manager.email"


async def test_add_one_manager_invalid_email_symbols(auth_ac: AsyncClient):
    response = await auth_ac.post("/manufacturer_managers", json={
        "first_name": "Иван",
        "second_name": "Иванов",
        "last_name": "Иванович",
        "phone": "+77856548569",
        "email": "test.com",
        "manufacturer_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for email field"


async def test_get_list_managers(auth_ac: AsyncClient):
    response = await auth_ac.get("/manufacturer_managers")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2


async def test_get_one_manager(auth_ac: AsyncClient):
    response = await auth_ac.get("/manufacturer_managers/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_edit_one_manager(auth_ac: AsyncClient):
    response = await auth_ac.patch("/manufacturer_managers/2", json={"first_name": "Виктор"})

    assert response.status_code == 200
    assert response.json()["first_name"] == "Виктор"
    assert response.json()["id"] == 2


async def test_edit_one_manager_invalid_manufacturer(auth_ac: AsyncClient):
    response = await auth_ac.patch("/manufacturer_managers/2", json={"manufacturer_id": "55"})

    assert response.status_code == 404
    assert response.json()["detail"] == 'Manufacturer with this id not found'


async def test_delete_one_manager(auth_ac: AsyncClient):
    response = await auth_ac.delete("/manufacturer_managers/2")

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
