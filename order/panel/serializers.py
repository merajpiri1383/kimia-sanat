from rest_framework import serializers
from order.panel.models import ListShopPage,OrderPage


class OrderPageSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = OrderPage
        exclude = ["id"]

class ListShopPageSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = ListShopPage
        exclude = ["id"]