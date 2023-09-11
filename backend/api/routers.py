from api.store.category import router as router_store_category
from api.store.product import router as router_store_product
from api.store.customer import router as router_store_customer
from api.store.customer_manager import router as router_store_customer_manager
from api.store.manufacturer import router as router_store_manufacturer
from api.store.manufacturer_manager import router as router_store_manufacturer_manager
from api.store.staff_manager import router as router_store_staff_manager
from api.store.image import router as router_store_image
from api.store.order import router as router_store_order
from api.store.review import router as router_store_review

from api.auth.user import router as router_auth_user
from api.auth.auth import router as router_auth_auth

all_routers = [
    router_store_category,
    router_store_product,
    router_store_customer,
    router_store_customer_manager,
    router_store_manufacturer,
    router_store_manufacturer_manager,
    router_store_staff_manager,
    router_store_image,
    router_store_order,
    router_store_review,
    router_auth_user,
    router_auth_auth
]
