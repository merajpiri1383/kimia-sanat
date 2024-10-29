from rest_framework import serializers
from order.panel.models import ListShopPage,OrderPage,MyOrderPage


class OrderPageSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = OrderPage
        exclude = ["id"]

class ListShopPageSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = ListShopPage
        exclude = ["id"]

class MyOrderPageSerializer (serializers.ModelSerializer) : 
    
    class Meta : 
        model = MyOrderPage
        exclude = ["id"]