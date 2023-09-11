from httpx import AsyncClient


async def test_add_one_order(auth_ac: AsyncClient):
    response = await auth_ac.post("/orders", json={
        "delivery_method": "Доставка",
        "payment_method": "Наличными",
        "staff_manager_id": 1,
        "customer_id": 1,
        "products": {
            "1": 2,
            "2": 5
        }
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2
    assert response.json()["sum_price"] == 95


async def test_add_one_order_2(auth_ac: AsyncClient):
    response = await auth_ac.post("/orders", json={
        "delivery_method": "Доставка",
        "payment_method": "Наличными",
        "staff_manager_id": 1,
        "customer_id": 1,
        "products": {
            "2": 7
        }
    })

    assert response.status_code == 200
    assert response.json()["id"] == 3
    assert response.json()["sum_price"] == 105


async def test_add_one_order_invalid_staff_manager(auth_ac: AsyncClient):
    response = await auth_ac.post("/orders", json={
        "delivery_method": "Доставка",
        "payment_method": "Наличными",
        "staff_manager_id": 55,
        "customer_id": 1,
        "products": {
            "2": 7
        }
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Staff manager with this id not found'


async def test_add_one_order_invalid_customer(auth_ac: AsyncClient):
    response = await auth_ac.post("/orders", json={
        "delivery_method": "Доставка",
        "payment_method": "Наличными",
        "staff_manager_id": 1,
        "customer_id": 55,
        "products": {
            "2": 7
        }
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Customer with this id not found'


async def test_add_one_order_invalid_product(auth_ac: AsyncClient):
    response = await auth_ac.post("/orders", json={
        "delivery_method": "Доставка",
        "payment_method": "Наличными",
        "staff_manager_id": 1,
        "customer_id": 1,
        "products": {
            "5": 7
        }
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Product with this id not found'


async def test_get_list_orders(auth_ac: AsyncClient):
    response = await auth_ac.get("/orders")

    assert response.status_code == 200
    assert response.json()[2]["id"] == 3
    assert len(response.json()) == 3


async def test_get_one_order(auth_ac: AsyncClient):
    response = await auth_ac.get("/orders/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_edit_one_order(auth_ac: AsyncClient):
    response = await auth_ac.patch("/orders/2", json={"products": {"1": 5}})

    assert response.status_code == 200
    assert response.json()["products"][0]["id"] == 1
    assert response.json()["sum_price"] == 50


async def test_edit_one_order_no_product(auth_ac: AsyncClient):
    response = await auth_ac.patch("/orders/2", json={"status": "Выполнено"})

    assert response.status_code == 200
    assert response.json()["status"] == "Выполнено"
    assert response.json()["sum_price"] == 50


async def test_edit_one_order_invalid_staffmanager(auth_ac: AsyncClient):
    response = await auth_ac.patch("/orders/2", json={"staff_manager_id": 55})

    assert response.status_code == 404
    assert response.json()["detail"] == 'Staff manager with this id not found'


async def test_edit_one_order_invalid_customer(auth_ac: AsyncClient):
    response = await auth_ac.patch("/orders/2", json={"customer_id": 55})

    assert response.status_code == 404
    assert response.json()["detail"] == 'Customer with this id not found'


async def test_edit_one_order_invalid_product(auth_ac: AsyncClient):
    response = await auth_ac.patch("/orders/2", json={"products": {"55": 1}})

    assert response.status_code == 404
    assert response.json()["detail"] == 'Product with this id not found'


async def test_delete_one_order(auth_ac: AsyncClient):
    response = await auth_ac.delete("/orders/2")

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
