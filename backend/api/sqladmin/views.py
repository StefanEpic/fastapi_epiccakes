from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from dotenv import load_dotenv
import os

from views.sqladmin import UserAdmin as view_user
from views.sqladmin import PermissionAdmin as view_permission
from views.sqladmin import CategoryAdmin as view_category
from views.sqladmin import ProductAdmin as view_product
from views.sqladmin import ImageAdmin as view_image
from views.sqladmin import ManufacturerAdmin as view_manufacturer
from views.sqladmin import ManufacturerManagerAdmin as view_manufacturermanager
from views.sqladmin import CustomerAdmin as view_customer
from views.sqladmin import CustomerManagerAdmin as view_customermanager
from views.sqladmin import StaffManagerAdmin as view_staffmanager
from views.sqladmin import OrderAdmin as view_order
from views.sqladmin import ReviewAdmin as view_review

all_views = [
    view_user,
    view_permission,
    view_category,
    view_product,
    view_image,
    view_manufacturer,
    view_manufacturermanager,
    view_customer,
    view_customermanager,
    view_staffmanager,
    view_order,
    view_review
]

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
        if "token" not in request.session:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)


authentication_backend = AdminAuth(secret_key=SQLADMIN_TOKEN)
