from rest_framework import serializers
from order.models import Order,PaySlip,PreInvoice,PreInvoiceProduct
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

    products_count = CountSerializer(many=True)

    pay_slips = PaySlipSerializer(many=True)


    class Meta :  
        model = Order
        fields = "__all__"
        read_only_fields = ["tracking_code"]
    
# مدل ساده سفارش 
class OrderSimpleSerializer (serializers.ModelSerializer) : 

    class Meta :  
        model = Order
        exclude = ["products_count","user"] 


# مدل پیش فاکتور 

class PreInvoiceProductSerializer (serializers.ModelSerializer) : 

    title = serializers.SerializerMethodField("get_title")

    def get_title(self,obj) : 
        return obj.title.name

    class Meta : 
        model = PreInvoiceProduct
        exclude = ["id"]


class PreInvoiceSerializer (serializers.ModelSerializer) : 

    products = PreInvoiceProductSerializer(many=True)

    class Meta : 
        model = PreInvoice
        exclude = ["id","is_for_collegue","is_for_customer"]