from sqladmin import ModelView

from models.store.manufacturer import Manufacturer


# class CategoryAdmin(ModelView, model=Category):
#     column_list = "__all__"
#     form_columns = "__all__"
#     column_details_list = "__all__"
#
#
# class TypeAdmin(ModelView, model=Type):
#     column_list = "__all__"
#     form_columns = "__all__"
#     column_details_list = "__all__"
#
#
# class ProductAdmin(ModelView, model=Product):
#     column_list = "__all__"
#     form_columns = "__all__"
#     column_details_list = "__all__"
#
#
# class ImageAdmin(ModelView, model=Image):
#     column_list = "__all__"
#     form_columns = "__all__"
#     column_details_list = "__all__"


class ManufacturerAdmin(ModelView, model=Manufacturer):
    column_list = "__all__"
    form_columns = "__all__"
    column_details_list = "__all__"

#
# class ManufacturerManagerAdmin(ModelView, model=ManufacturerManager):
#     column_list = "__all__"
#     form_columns = "__all__"
#     column_details_list = "__all__"
#
#
# class ClientAdmin(ModelView, model=Client):
#     column_list = "__all__"
#     form_columns = "__all__"
#     column_details_list = "__all__"
#
#
# class ClientManagerAdmin(ModelView, model=ClientManager):
#     column_list = "__all__"
#     form_columns = "__all__"
#     column_details_list = "__all__"
#
#
# class StaffManagerAdmin(ModelView, model=StaffManager):
#     column_list = "__all__"
#     form_columns = "__all__"
#     column_details_list = "__all__"
#
#
# class OrderAdmin(ModelView, model=Order):
#     column_list = "__all__"
#     form_columns = "__all__"
#     column_details_list = "__all__"
#
#
# class ReviewAdmin(ModelView, model=Review):
#     column_list = "__all__"
#     form_columns = "__all__"
#     column_details_list = "__all__"
