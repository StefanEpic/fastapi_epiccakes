from httpx import AsyncClient


async def test_add_one_review(ac: AsyncClient):
    response = await ac.post("/reviews", json={
        "rating": 3,
        "text": "Спасибо! Было вкусно!",
        "order_id": 1,
        "customer_id": 1
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_add_one_review_invalid_order(ac: AsyncClient):
    response = await ac.post("/reviews", json={
        "rating": 3,
        "text": "Спасибо! Было вкусно!",
        "order_id": 55,
        "customer_id": 1
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Order with this id not found'


async def test_add_one_review_invalid_customer(ac: AsyncClient):
    response = await ac.post("/reviews", json={
        "rating": 3,
        "text": "Спасибо! Было вкусно!",
        "order_id": 1,
        "customer_id": 55
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'Customer with this id not found'


async def test_add_one_review_invalid_mapping_order_customer(ac: AsyncClient):
    response = await ac.post("/reviews", json={
        "rating": 3,
        "text": "Спасибо! Было вкусно!",
        "order_id": 1,
        "customer_id": 2
    })

    assert response.status_code == 404
    assert response.json()["detail"] == 'This order has a different id customer'


async def test_add_one_review_invalid_rating(ac: AsyncClient):
    response = await ac.post("/reviews", json={
        "rating": 8,
        "text": "Спасибо! Было вкусно!",
        "order_id": 1,
        "customer_id": 1
    })

    assert response.status_code == 200
    assert response.json()["detail"] == 'Error. Invalid value for rating field'


async def test_get_list_reviews(ac: AsyncClient):
    response = await ac.get("/reviews")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2


async def test_get_one_review(ac: AsyncClient):
    response = await ac.get("/reviews/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_edit_one_review(ac: AsyncClient):
    response = await ac.patch("/reviews/2", json={"text": "Очень доволен!"})

    assert response.status_code == 200
    assert response.json()["text"] == "Очень доволен!"


async def test_delete_one_review(ac: AsyncClient):
    response = await ac.delete("/reviews/2")

    assert response.status_code == 200
    assert response.json()["result"] == "success"
