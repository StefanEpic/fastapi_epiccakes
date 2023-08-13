from httpx import AsyncClient


async def test_add_one_category(ac: AsyncClient):
    response = await ac.post("/categories", json={
        "title": "С ягодами"
    })

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_add_one_category_invalid_title_unique(ac: AsyncClient):
    response = await ac.post("/categories", json={
        "title": "С ягодами"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: category.title"


async def test_get_list_categories(ac: AsyncClient):
    response = await ac.get("/categories")

    assert response.status_code == 200
    assert response.json()[1]["id"] == 2
    assert len(response.json()) == 2


async def test_get_one_category(ac: AsyncClient):
    response = await ac.get("/categories/2")

    assert response.status_code == 200
    assert response.json()["id"] == 2


async def test_edit_one_category(ac: AsyncClient):
    response = await ac.patch("/categories/2", json={"title": "Шоколадные"})

    assert response.status_code == 200
    assert response.json()["title"] == "Шоколадные"
    assert response.json()["id"] == 2


async def test_delete_one_category(ac: AsyncClient):
    response = await ac.delete("/categories/2")

    assert response.status_code == 200
    assert response.json()["result"] == "success"
