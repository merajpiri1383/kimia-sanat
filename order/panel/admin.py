from django.contrib import admin
from order.panel.models import OrderPage,ListShopPage


@admin.register(OrderPage)
class OrderPageAdmin (admin.ModelAdmin) : 
    exclude = ["id"]


@admin.register(ListShopPage)
class ListShopPageAdmin (admin.ModelAdmin) : 
    exclude = ["id"]