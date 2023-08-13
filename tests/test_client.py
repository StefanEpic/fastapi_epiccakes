from httpx import AsyncClient


async def test_add_one_client(ac: AsyncClient):
    response = await ac.post("/clients", json={
        "title": "ИП Вкусно",
        "city": "Москва",
        "street": "Главная",
        "house": "34",
        "status": "Действующий",
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_add_one_client_unique(ac: AsyncClient):
    response = await ac.post("/clients", json={
        "title": "ИП Вкусно",
        "city": "Москва",
        "street": "Главная",
        "house": "34",
        "status": "Действующий",
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: client.title"


async def test_get_list_clients(ac: AsyncClient):
    response = await ac.get("/clients")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2


async def test_get_one_client(ac: AsyncClient):
    response = await ac.get("/clients/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_get_one_client_with_managers(ac: AsyncClient):
    response = await ac.get("/clients/1")

    assert response.status_code == 200
    assert response.json()["managers"][0]["first_name"] == "Виктор"


async def test_edit_one_client(ac: AsyncClient):
    response = await ac.patch("/clients/2", json={"title": "ИП Здорово"})

    assert response.status_code == 200
    assert response.json()["title"] == "ИП Здорово"
    assert response.json()["id"] == 2


async def test_delete_one_client(ac: AsyncClient):
    response = await ac.delete("/clients/2")

    assert response.status_code == 200
    assert response.json()["result"] == "success"
