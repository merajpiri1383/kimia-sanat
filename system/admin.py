from django.contrib import admin
from system.models import GroupProduct,ProductSystem
from system.resource import ProductSystemResource
from import_export.admin import ExportMixin


@admin.register(GroupProduct)
class GroupProductAdmin (admin.ModelAdmin) : 
    exclude = ["id"]


@admin.register(ProductSystem)
class ProductSystemAdmin (ExportMixin,admin.ModelAdmin) : 
    exclude = ["id"]
    resource_class = ProductSystemResource