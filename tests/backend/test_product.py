from httpx import AsyncClient


async def test_add_one_product(auth_ac: AsyncClient):
    response = await auth_ac.post("/products", json={
        "title": "Медовик",
        "type": "Бисквитные",
        "price": 20,
        "manufacturer_id": 1,
        "categories": [1, 2]
    })

    assert response.status_code == 200
    assert response.json()["id"] == 3


async def test_add_one_product_unique(auth_ac: AsyncClient):
    response = await auth_ac.post("/products", json={
        "title": "Медовик",
        "type": "Бисквитные",
        "price": 20,
        "manufacturer_id": 1,
        "categories": [1, 2]
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: product.title"


async def test_add_one_product_invalid_manufacturer(auth_ac: AsyncClient):
    response = await auth_ac.post("/products", json={
        "title": "Муравейник",
        "type": "Бисквитные",
        "price": 20,
        "manufacturer_id": 55,
        "categories": [1, 2]
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Manufacturer with this id not found'


async def test_add_one_product_invalid_category(auth_ac: AsyncClient):
    response = await auth_ac.post("/products", json={
        "title": "Муравейник",
        "type": "Бисквитные",
        "price": 20,
        "manufacturer_id": 1,
        "categories": [5, 6]
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Category with this id not found'


async def test_get_list_products(ac: AsyncClient):
    response = await ac.get("/products")

    assert response.status_code == 200
    assert response.json()[2]["id"] == 3
    assert len(response.json()) == 3


async def test_get_one_product(ac: AsyncClient):
    response = await ac.get("/products/3")

    assert response.status_code == 200
    assert response.json()["id"] == 3


async def test_edit_one_product(auth_ac: AsyncClient):
    response = await auth_ac.patch("/products/3", json={"title": "Радость", "categories": [2]})

    assert response.status_code == 200
    assert response.json()["title"] == "Радость"
    assert response.json()["categories"] == [{'title': 'Эксклюзив', 'description': None, 'id': 2}]
    assert response.json()["id"] == 3


async def test_edit_one_product_invalid_manufacturer(auth_ac: AsyncClient):
    response = await auth_ac.patch("/products/3", json={"manufacturer_id": 55})

    assert response.status_code == 404
    assert response.json()["detail"] == 'Manufacturer with this id not found'


async def test_edit_one_product_invalid_category(auth_ac: AsyncClient):
    response = await auth_ac.patch("/products/3", json={"categories": [5, 6]})

    assert response.status_code == 404
    assert response.json()["detail"] == 'Category with this id not found'


async def test_edit_one_product_invalid_unique(auth_ac: AsyncClient):
    response = await auth_ac.patch("/products/2", json={"title": "Бисквитный пирог"})

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: product.title"


async def test_delete_one_product(auth_ac: AsyncClient):
    response = await auth_ac.delete("/products/3")

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
