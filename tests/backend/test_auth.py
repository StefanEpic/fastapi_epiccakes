from httpx import AsyncClient


async def test_login_logout(ac: AsyncClient):
    response = await ac.post("/token",
                             data={
                                 "username": "admin@admin.com",
                                 "password": "12345"
                             },
                             headers={"content-type": "application/x-www-form-urlencoded"})

    assert response.status_code == 200

    assert "access_token" in response.json()
    assert "token_type" in response.json()

    response = await ac.get("/logout", headers={"Authorization": f"Bearer {response.json()['access_token']}"})

    assert response.status_code == 200
    assert response.json()["detail"] == "success"


async def test_login_invalid_password(ac: AsyncClient):
    response = await ac.post("/token",
                             data={
                                 "username": "admin@admin.com",
                                 "password": "123456"
                             },
                             headers={"content-type": "application/x-www-form-urlencoded"})

    assert response.status_code == 200
    assert response.json()["detail"] == "Incorrect username or password"
