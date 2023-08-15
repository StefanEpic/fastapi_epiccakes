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
