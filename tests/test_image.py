import os

from httpx import AsyncClient
from conftest import client


async def test_add_one_image():
    filepath = f'{os.path.abspath(os.curdir)}/tests/testfile.jpg'
    with open(filepath, "rb") as image:
        response = client.post("/images", params={"product_id": 1}, files={"image": image})

        assert response.status_code == 200
        assert response.json()["title"] == image.name.split('/')[-1]
        assert response.json()["id"] == 1


async def test_add_one_image_invalid_product(ac: AsyncClient):
    filepath = f'{os.path.abspath(os.curdir)}/tests/testfile.jpg'
    with open(filepath, "rb") as image:
        response = client.post("/images", params={"product_id": 3}, files={"image": image})

        assert response.status_code == 404
        assert response.json()["detail"] == 'Product with this id not found'


async def test_add_one_image_title_unique():
    filepath = f'{os.path.abspath(os.curdir)}/tests/testfile.jpg'
    with open(filepath, "rb") as image:
        response = client.post("/images", params={"product_id": 1}, files={"image": image})

        assert response.status_code == 200
        assert response.json()["detail"] == 'UNIQUE constraint failed: image.title'


async def test_get_list_images(ac: AsyncClient):
    response = await ac.get("/images")

    assert response.status_code == 200
    assert response.json()[0]["id"] == 1
    assert len(response.json()) == 1


async def test_get_one_image(ac: AsyncClient):
    response = await ac.get("/images/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


async def test_delete_one_image(ac: AsyncClient):
    response = await ac.delete("/images/1")

    assert response.status_code == 200
    assert response.json()["result"] == "success"
