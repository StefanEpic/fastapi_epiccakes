from httpx import AsyncClient


async def test_add_one_customer(auth_ac: AsyncClient):
    response = await auth_ac.post("/customers", json={
        "title": "ИП Вкусно",
        "city": "Москва",
        "street": "Главная",
        "house": "34",
        "metro_station": "Центральная",
        "status": "Действующий",
    })

    assert response.status_code == 200
    assert response.json()["id"] == 3


async def test_add_one_customer_unique(auth_ac: AsyncClient):
    response = await auth_ac.post("/customers", json={
        "title": "ИП Вкусно",
        "city": "Москва",
        "street": "Главная",
        "house": "34",
        "status": "Действующий",
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: customer.title"


async def test_get_list_customers(auth_ac: AsyncClient):
    response = await auth_ac.get("/customers")

    assert response.status_code == 200
    assert response.json()[2]["id"] == 3
    assert len(response.json()) == 3


async def test_get_list_customers_with_filter(auth_ac: AsyncClient):
    response = await auth_ac.get("/customers", params={
        "city": "Москва",
        "street": "Главная",
        "metro_station": "Центральная"
    })

    assert response.status_code == 200
    assert response.json()[0]["id"] == 3
    assert len(response.json()) == 1


async def test_get_one_customer(auth_ac: AsyncClient):
    response = await auth_ac.get("/customers/3")

    assert response.status_code == 200
    assert response.json()["id"] == 3


async def test_get_one_customer_with_managers(auth_ac: AsyncClient):
    response = await auth_ac.get("/customers/1")

    assert response.status_code == 200
    assert response.json()["managers"][0]["first_name"] == "Виктор"


async def test_edit_one_customer(auth_ac: AsyncClient):
    response = await auth_ac.patch("/customers/3", json={"title": "ИП Здорово"})

    assert response.status_code == 200
    assert response.json()["title"] == "ИП Здорово"
    assert response.json()["id"] == 3


async def test_delete_one_customer(auth_ac: AsyncClient):
    response = await auth_ac.delete("/customers/3")

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
