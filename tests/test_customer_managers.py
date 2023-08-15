from httpx import AsyncClient


async def test_add_one_manager(ac: AsyncClient):
    response = await ac.post("/customer_managers", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+77777777777",
        "email": "boris@test.com",
        "customer_id": 1
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_add_one_manager_invalid_customer(ac: AsyncClient):
    response = await ac.post("/customer_managers", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+77777777777",
        "email": "boris@test.com",
        "customer_id": 55
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Customer with this id not found'


async def test_add_one_manager_invalid_name(ac: AsyncClient):
    response = await ac.post("/customer_managers", json={
        "first_name": "Борис333",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+77777777777",
        "email": "boris@test.com",
        "customer_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for name field"


async def test_add_one_manager_invalid_phone_unique(ac: AsyncClient):
    response = await ac.post("/customer_managers", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+77777777777",
        "email": "boris2@test.com",
        "customer_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: customermanager.phone"


async def test_add_one_manager_invalid_phone_text(ac: AsyncClient):
    response = await ac.post("/customer_managers", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "asd",
        "email": "boris2@test.com",
        "customer_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for phone field"


async def test_add_one_manager_invalid_email_unique(ac: AsyncClient):
    response = await ac.post("/customer_managers", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+77777777778",
        "email": "boris@test.com",
        "customer_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: customermanager.email"


async def test_add_one_manager_invalid_email_symbols(ac: AsyncClient):
    response = await ac.post("/customer_managers", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+77777777778",
        "email": "test.com",
        "customer_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for email field"


async def test_get_list_managers(ac: AsyncClient):
    response = await ac.get("/customer_managers")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2


async def test_get_one_manager(ac: AsyncClient):
    response = await ac.get("/customer_managers/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_edit_one_manager(ac: AsyncClient):
    response = await ac.patch("/customer_managers/2", json={"first_name": "Виктор"})

    assert response.status_code == 200
    assert response.json()["first_name"] == "Виктор"
    assert response.json()["id"] == 2


async def test_edit_one_manager_invalid_customer(ac: AsyncClient):
    response = await ac.patch("/customer_managers/2", json={"customer_id": "55"})

    assert response.status_code == 404
    assert response.json()["detail"] == 'Customer with this id not found'


async def test_delete_one_manager(ac: AsyncClient):
    response = await ac.delete("/customer_managers/2")

    assert response.status_code == 200
    assert response.json()["result"] == "success"
