from httpx import AsyncClient


async def test_add_one_manufacturer(ac: AsyncClient):
    response = await ac.post("/manufacturers", json={
        "title": "ИП Вкусно",
        "city": "Москва",
        "street": "Главная",
        "house": "34",
        "status": "Действующий",
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_add_one_manufacturer_unique(ac: AsyncClient):
    response = await ac.post("/manufacturers", json={
        "title": "ИП Вкусно",
        "city": "Москва",
        "street": "Главная",
        "house": "34",
        "status": "Действующий",
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: manufacturer.title"


async def test_get_list_manufacturers(ac: AsyncClient):
    response = await ac.get("/manufacturers")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2


async def test_get_one_manufacturer(ac: AsyncClient):
    response = await ac.get("/manufacturers/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_get_one_manufacturer_with_managers(ac: AsyncClient):
    response = await ac.get("/manufacturers/1")

    assert response.status_code == 200
    assert response.json()["managers"][0]["first_name"] == "Иван"


async def test_edit_one_manufacturer(ac: AsyncClient):
    response = await ac.patch("/manufacturers/2", json={"title": "ИП Здорово"})

    assert response.status_code == 200
    assert response.json()["title"] == "ИП Здорово"
    assert response.json()["id"] == 2


async def test_delete_one_manufacturer(ac: AsyncClient):
    response = await ac.delete("/manufacturers/2")

    assert response.status_code == 200
    assert response.json()["result"] == "success"
