from sqladmin import ModelView

from models.auth import User, Permission
from models.store import Category, Product, Image, Customer, CustomerManager, Manufacturer, ManufacturerManager, Order, \
    Review, StaffManager


class UserAdmin(ModelView, model=User):
    column_list = "__all__"
    form_columns = "__all__"
    column_details_list = "__all__"
    can_export = False


class PermissionAdmin(ModelView, model=Permission):
    column_list = "__all__"
    form_excluded_columns = [Permission.users]
    column_details_list = "__all__"
    can_export = False


class CategoryAdmin(ModelView, model=Category):
    column_list = "__all__"
    form_excluded_columns = [Category.products]
    column_details_list = "__all__"
    name_plural = "Categories"
    can_export = False


class ProductAdmin(ModelView, model=Product):
    column_list = "__all__"
    form_excluded_columns = [Product.images]
    column_details_list = "__all__"
    can_export = False


class ImageAdmin(ModelView, model=Image):
    column_list = "__all__"
    form_columns = "__all__"
    column_details_list = "__all__"
    can_export = False


class CustomerAdmin(ModelView, model=Customer):
    column_list = "__all__"
    form_excluded_columns = [Customer.managers, Customer.orders, Customer.reviews]
    column_details_list = "__all__"
    can_export = False


class CustomerManagerAdmin(ModelView, model=CustomerManager):
    column_list = "__all__"
    form_columns = "__all__"
    column_details_list = "__all__"
    can_export = False


class ManufacturerAdmin(ModelView, model=Manufacturer):
    column_list = "__all__"
    form_excluded_columns = [Manufacturer.managers, Manufacturer.products]
    column_details_list = "__all__"
    can_export = False


class ManufacturerManagerAdmin(ModelView, model=ManufacturerManager):
    column_list = "__all__"
    form_columns = "__all__"
    column_details_list = "__all__"
    can_export = False


class OrderAdmin(ModelView, model=Order):
    column_list = "__all__"
    form_excluded_columns = [Order.reviews]
    column_details_list = "__all__"
    can_export = False


class ReviewAdmin(ModelView, model=Review):
    column_list = "__all__"
    form_columns = "__all__"
    column_details_list = "__all__"
    can_export = False


class StaffManagerAdmin(ModelView, model=StaffManager):
    column_list = "__all__"
    form_excluded_columns = [StaffManager.orders]
    column_details_list = "__all__"
    can_export = False
