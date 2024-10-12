from django.contrib import admin
from system.models import GroupProduct,ProductSystem


@admin.register(GroupProduct)
class GroupProductAdmin (admin.ModelAdmin) : 
    exclude = ["id"]


@admin.register(ProductSystem)
class ProductSystemAdmin (admin.ModelAdmin) : 
    exclude = ["id"]