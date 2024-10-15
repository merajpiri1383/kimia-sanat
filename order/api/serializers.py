from rest_framework import serializers
from order.models import Order,PaySlip,PreInvoice,PreInvoiceProduct
from product.api.serializers import CountSerializer
from rest_framework.exceptions import  ValidationError
import re


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

number_regex = re.compile("^[0-9]{8,}$")

# مدل فیش واریزی
class PaySlipSerializer (serializers.ModelSerializer) : 

    products = serializers.SerializerMethodField("get_products")

    tracking_code = serializers.SerializerMethodField("get_tracking_code")


    def get_tracking_code(self,obj) : 
        return obj.order.tracking_code

    def get_products(self,obj) : 
        if hasattr(obj.order,"pre_invoice") : 
            product_list = obj.order.pre_invoice.products.all()
            return PreInvoiceProductSerializer(product_list,many=True).data
        return None

    class Meta : 
        model = PaySlip
        fields = "__all__"


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