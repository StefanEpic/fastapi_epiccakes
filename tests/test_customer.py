from httpx import AsyncClient


async def test_add_one_customer(ac: AsyncClient):
    response = await ac.post("/customers", json={
        "title": "ИП Вкусно",
        "city": "Москва",
        "street": "Главная",
        "house": "34",
        "status": "Действующий",
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_add_one_customer_unique(ac: AsyncClient):
    response = await ac.post("/customers", json={
        "title": "ИП Вкусно",
        "city": "Москва",
        "street": "Главная",
        "house": "34",
        "status": "Действующий",
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: customer.title"


async def test_get_list_customers(ac: AsyncClient):
    response = await ac.get("/customers")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2


async def test_get_one_customer(ac: AsyncClient):
    response = await ac.get("/customers/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_get_one_customer_with_managers(ac: AsyncClient):
    response = await ac.get("/customers/1")

    assert response.status_code == 200
    assert response.json()["managers"][0]["first_name"] == "Виктор"


async def test_edit_one_customer(ac: AsyncClient):
    response = await ac.patch("/customers/2", json={"title": "ИП Здорово"})

    assert response.status_code == 200
    assert response.json()["title"] == "ИП Здорово"
    assert response.json()["id"] == 2


async def test_delete_one_customer(ac: AsyncClient):
    response = await ac.delete("/customers/2")

    assert response.status_code == 200
    assert response.json()["result"] == "success"
