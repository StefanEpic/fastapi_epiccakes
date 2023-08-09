# from api.routers_store.category import router as router_store_category
from api.routers_store.product import router as router_store_product
from api.routers_store.client import router as router_store_client
from api.routers_store.client_manager import router as router_store_client_manager
from api.routers_store.manufacturer import router as router_store_manufacturer
from api.routers_store.manufacturer_manager import router as router_store_manufacturer_manager
# from api.routers_store.staff_manager import router as router_store_staff_manager

all_routers = [
    # router_store_category,
    router_store_product,
    router_store_client,
    router_store_client_manager,
    router_store_manufacturer,
    router_store_manufacturer_manager,
    # router_store_staff_manager
]
