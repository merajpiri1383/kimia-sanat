from rest_framework import serializers
from order.models import Order,PaySlip
from product.api.serializers import CountSerializer
from rest_framework.exceptions import  ValidationError
import re

number_regex = re.compile("^[0-9]{8,}$")

# مدل فیش واریزی
class PaySlipSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = PaySlip
        fields = "__all__"

    def validate(self,attrs) : 
        if not number_regex.findall(attrs.get("credit_card_number")) : 
            raise ValidationError({'credit_card_number' : 'creadit card number must be number and at least 8 character .'})
        if not number_regex.findall(attrs["iban"]) : 
            raise ValidationError({'iban' : 'iban must be number and at least 8 character .'})
        return super().validate(attrs)


# مدل سفارش 

class OrderSerializer (serializers.ModelSerializer) : 

    class Meta :  
        model = Order
        exclude = ["products","user","created"] 

    def to_representation(self,instance) : 
        context = super().to_representation(instance)
        context["created_date"] = instance.created.strftime('%Y-%m-%d')
        context["created_time"] = instance.created.strftime('%H:%M:%S')
        context["product"] = CountSerializer(
            instance.products.all(),
            many=True
        ).data
        context["pay_slips"] = PaySlipSerializer(
            instance.pay_slips.all(),
            many=True,
            context=self.context
        ).data
        return context
    
# مدل ساده سفارش 
class OrderSimpleSerializer (serializers.ModelSerializer) : 

    class Meta :  
        model = Order
        exclude = ["products","user","created"] 

    def to_representation(self,instance) : 
        context = super().to_representation(instance)
        context["created_date"] = instance.created.strftime('%Y-%m-%d')
        context["created_time"] = instance.created.strftime('%H:%M:%S')
        return context