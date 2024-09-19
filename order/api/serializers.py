from rest_framework import serializers
from order.models import Order
from product.api.serializers import CountSerializer

# مدل سفارش 

class OrderSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = Order
        exclude = ["products","user","created"]

    def to_representation(self,instance) : 
        context = super().to_representation(instance)
        context["created_date"] = instance.created.strftime('%Y-%m-%d')
        context["created_time"] = instance.created.strftime('%H:%M:%S')
        context["counts"] = CountSerializer(instance.products.all(),many=True).data
        return context