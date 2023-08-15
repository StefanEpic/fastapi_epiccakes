from httpx import AsyncClient


async def test_add_one_order(ac: AsyncClient):
    response = await ac.post("/orders", json={
        "delivery_method": "Доставка",
        "payment_method": "Наличными",
        "status": "В работе",
        "staffmanager_id": 1,
        "customer_id": 1,
        "products": {
            "1": 2,
            "2": 5
        }
    })

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["sum_price"] == 95


async def test_add_one_order_2(ac: AsyncClient):
    response = await ac.post("/orders", json={
        "delivery_method": "Доставка",
        "payment_method": "Наличными",
        "status": "В работе",
        "staffmanager_id": 1,
        "customer_id": 1,
        "products": {
            "2": 7
        }
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2
    assert response.json()["sum_price"] == 105


async def test_add_one_order_invalid_staffmanager(ac: AsyncClient):
    response = await ac.post("/orders", json={
        "delivery_method": "Доставка",
        "payment_method": "Наличными",
        "status": "В работе",
        "staffmanager_id": 55,
        "customer_id": 1,
        "products": {
            "2": 7
        }
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Staff manager with this id not found'


async def test_add_one_order_invalid_customer(ac: AsyncClient):
    response = await ac.post("/orders", json={
        "delivery_method": "Доставка",
        "payment_method": "Наличными",
        "status": "В работе",
        "staffmanager_id": 1,
        "customer_id": 55,
        "products": {
            "2": 7
        }
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Customer with this id not found'


async def test_add_one_order_invalid_product(ac: AsyncClient):
    response = await ac.post("/orders", json={
        "delivery_method": "Доставка",
        "payment_method": "Наличными",
        "status": "В работе",
        "staffmanager_id": 1,
        "customer_id": 1,
        "products": {
            "5": 7
        }
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Product with this id not found'


async def test_get_list_orders(ac: AsyncClient):
    response = await ac.get("/orders")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2


async def test_get_one_order(ac: AsyncClient):
    response = await ac.get("/orders/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_edit_one_order(ac: AsyncClient):
    response = await ac.patch("/orders/2", json={"products": {"1": 5}})

    assert response.status_code == 200
    assert response.json()["products"][0]["id"] == 1
    assert response.json()["sum_price"] == 50


async def test_edit_one_order_no_product(ac: AsyncClient):
    response = await ac.patch("/orders/2", json={"status": "Выполнено"})

    assert response.status_code == 200
    assert response.json()["status"] == "Выполнено"
    assert response.json()["sum_price"] == 50


async def test_edit_one_order_invalid_staffmanager(ac: AsyncClient):
    response = await ac.patch("/orders/2", json={"staffmanager_id": 55})

    assert response.status_code == 404
    assert response.json()["detail"] == 'Staff manager with this id not found'


async def test_edit_one_order_invalid_customer(ac: AsyncClient):
    response = await ac.patch("/orders/2", json={"customer_id": 55})

    assert response.status_code == 404
    assert response.json()["detail"] == 'Customer with this id not found'


async def test_edit_one_order_invalid_product(ac: AsyncClient):
    response = await ac.patch("/orders/2", json={"products": {"55": 1}})

    assert response.status_code == 404
    assert response.json()["detail"] == 'Product with this id not found'


async def test_delete_one_order(ac: AsyncClient):
    response = await ac.delete("/orders/1")

    assert response.status_code == 200
    assert response.json()["result"] == "success"
