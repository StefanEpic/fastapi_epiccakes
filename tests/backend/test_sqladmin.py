from httpx import AsyncClient


async def test_login_logout(ac: AsyncClient):
    response = await ac.post("/admin/login",
                             data={
                                 "username": "admin@admin.com",
                                 "password": "12345"
                             })

    assert response.status_code == 302

    response = await ac.get("/logout", headers={"Authorization": f"Bearer {response.cookies['session']}"})

    assert response.status_code == 200
