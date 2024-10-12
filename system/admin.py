from django.contrib import admin
from system.models import GroupProduct,ProductSystem
from import_export.admin import ExportActionMixin


@admin.register(GroupProduct)
class GroupProductAdmin (admin.ModelAdmin) : 
    exclude = ["id"]


@admin.register(ProductSystem)
class ProductSystemAdmin (ExportActionMixin,admin.ModelAdmin) : 
    exclude = ["id"]