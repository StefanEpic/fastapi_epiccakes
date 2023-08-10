from views.sqladmin import CategoryAdmin as view_category
from views.sqladmin import TypeAdmin as view_type
from views.sqladmin import ProductAdmin as view_product
from views.sqladmin import ImageAdmin as view_image
from views.sqladmin import ManufacturerAdmin as view_manufacturer
from views.sqladmin import ManufacturerManagerAdmin as view_manufacturermanager
from views.sqladmin import ClientAdmin as view_client
from views.sqladmin import ClientManagerAdmin as view_clientmanager
from views.sqladmin import StaffManagerAdmin as view_staffmanager
from views.sqladmin import OrderAdmin as view_order
from views.sqladmin import ReviewAdmin as view_review

all_views = [
    view_category,
    view_type,
    view_product,
    view_image,
    view_manufacturer,
    view_manufacturermanager,
    view_client,
    view_clientmanager,
    view_staffmanager,
    view_order,
    view_review
]
