from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from dotenv import load_dotenv
import os

load_dotenv()

SQLADMIN_USER = os.environ.get('SQLADMIN_USER')
SQLADMIN_PASSWORD = os.environ.get('SQLADMIN_PASSWORD')
SQLADMIN_TOKEN = os.environ.get('SQLADMIN_TOKEN')


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        if username == SQLADMIN_USER and password == SQLADMIN_PASSWORD:
            request.session.update({"token": SQLADMIN_TOKEN})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        if not "token" in request.session:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)


authentication_backend = AdminAuth(secret_key=SQLADMIN_TOKEN)
