from rest_framework import serializers
from order.models import Cart,CartProduct

# مدل سبد خرید
class CartSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Cart
        fields = "__all__"