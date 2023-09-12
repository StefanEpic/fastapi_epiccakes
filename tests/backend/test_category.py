from httpx import AsyncClient


async def test_add_one_category(auth_ac: AsyncClient):
    response = await auth_ac.post("/categories", json={
        "title": "С ягодами"
    })

    assert response.status_code == 200
    assert response.json()["id"] == 4


async def test_add_one_category_invalid_title_unique(auth_ac: AsyncClient):
    response = await auth_ac.post("/categories", json={
        "title": "С ягодами"
    })

    assert response.status_code == 200
    assert response.json()["detail"] == "UNIQUE constraint failed: category.title"


async def test_get_list_categories(ac: AsyncClient):
    response = await ac.get("/categories")

    assert response.status_code == 200
    assert response.json()[3]["id"] == 4
    assert len(response.json()) == 4


async def test_get_one_category(ac: AsyncClient):
    response = await ac.get("/categories/4")

    assert response.status_code == 200
    assert response.json()["id"] == 4


async def test_edit_one_category(auth_ac: AsyncClient):
    response = await auth_ac.patch("/categories/4", json={"title": "Шоколадные"})

    assert response.status_code == 200
    assert response.json()["title"] == "Шоколадные"
    assert response.json()["id"] == 4


async def test_delete_one_category(auth_ac: AsyncClient):
    response = await auth_ac.delete("/categories/4")

    assert response.status_code == 200
    assert response.json()["detail"] == "success"
