from api.routers_store.category import router as router_store_category
from api.routers_store.product import router as router_store_product
from api.routers_store.customer import router as router_store_customer
from api.routers_store.customer_manager import router as router_store_customer_manager
from api.routers_store.manufacturer import router as router_store_manufacturer
from api.routers_store.manufacturer_manager import router as router_store_manufacturer_manager
from api.routers_store.staff_manager import router as router_store_staff_manager
from api.routers_store.image import router as router_store_image
from api.routers_store.order import router as router_store_order
# from api.routers_store.review import router as router_store_review

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
    # router_store_review
]
