from httpx import AsyncClient


async def test_add_one_manager(ac: AsyncClient):
    response = await ac.post("/staff_managers", json={
        "first_name": "Кирилл",
        "second_name": "Смирнов",
        "last_name": "Кириллович",
        "phone": "+71111111112",
        "email": "kiril@test.com",
        "job_title": "Стажер"
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_add_one_manager_invalid_name(ac: AsyncClient):
    response = await ac.post("/staff_managers", json={
        "first_name": "Кирилл333",
        "second_name": "Смирнов",
        "last_name": "Кириллович",
        "phone": "+71111111112",
        "email": "kiril@test.com",
        "job_title": "Стажер"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for name field"


async def test_add_one_manager_invalid_phone_unique(ac: AsyncClient):
    response = await ac.post("/staff_managers", json={
        "first_name": "Кирилл",
        "second_name": "Смирнов",
        "last_name": "Кириллович",
        "phone": "+71111111111",
        "email": "kiril2@test.com",
        "job_title": "Стажер"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: staffmanager.phone"


async def test_add_one_manager_invalid_phone_text(ac: AsyncClient):
    response = await ac.post("/staff_managers", json={
        "first_name": "Кирилл",
        "second_name": "Смирнов",
        "last_name": "Кириллович",
        "phone": "asd",
        "email": "kiril2@test.com",
        "job_title": "Стажер"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for phone field"


async def test_add_one_manager_invalid_email_unique(ac: AsyncClient):
    response = await ac.post("/staff_managers", json={
        "first_name": "Кирилл",
        "second_name": "Смирнов",
        "last_name": "Кириллович",
        "phone": "+71111111112",
        "email": "kiril@test.com",
        "job_title": "Стажер"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: staffmanager.email"


async def test_add_one_manager_invalid_email_symbols(ac: AsyncClient):
    response = await ac.post("/staff_managers", json={
        "first_name": "Кирилл",
        "second_name": "Смирнов",
        "last_name": "Кириллович",
        "phone": "+71111111112",
        "email": "test.com",
        "job_title": "Стажер"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for email field"


async def test_get_list_managers(ac: AsyncClient):
    response = await ac.get("/staff_managers")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2


async def test_get_one_manager(ac: AsyncClient):
    response = await ac.get("/staff_managers/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_edit_one_manager(ac: AsyncClient):
    response = await ac.patch("/staff_managers/2", json={"first_name": "Виктор"})

    assert response.status_code == 200
    assert response.json()["first_name"] == "Виктор"
    assert response.json()["id"] == 2


async def test_edit_one_manager_invalid_name(ac: AsyncClient):
    response = await ac.patch("/staff_managers/2", json={"first_name": "Виктор777"})

    assert response.status_code == 200
    assert response.json()["detail"] == "Error. Invalid value for name field"


async def test_delete_one_manager(ac: AsyncClient):
    response = await ac.delete("/staff_managers/2")

    assert response.status_code == 200
    assert response.json()["result"] == "success"
