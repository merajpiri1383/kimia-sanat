from rest_framework import serializers
from order.models import Order,PaySlip,PreInvoice,PreInvoiceProduct,ProductCount
from rest_framework.exceptions import  ValidationError
import re
from product.api.serializers import ProductSimpleSerializer
from user.api.serializers import UserInfoSerializer


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


# مدل محصولات سفارش 

class ProductCountSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = ProductCount
        fields = "__all__"

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["product"] = ProductSimpleSerializer(instance.product,context=self.context).data
        return context 


# مدل سفارش 

class OrderSerializer (serializers.ModelSerializer) : 

    pay_slips = PaySlipSerializer(many=True,read_only=True)

    product_counts = ProductCountSerializer(many=True,read_only=True)

    user = UserInfoSerializer()


    class Meta :  
        model = Order
        fields = "__all__"
        read_only_fields = ["tracking_code","state","created","tracking_code","official_invoice","user","id"]
    
    def __init__(self,instance=None,**kwargs) :
        if instance : 
            kwargs["partial"] = True
        return super().__init__(instance,**kwargs) 
    
    def update(self, instance, validated_data):
        if instance.state != "pending" : 
            raise ValidationError({"state": "order cant be edit."})
        return super().update(instance, validated_data)
    
# مدل ساده سفارش 
class OrderSimpleSerializer (serializers.ModelSerializer) : 

    product_counts = ProductCountSerializer(many=True,read_only=True)

    class Meta :  
        model = Order
        fields = "__all__"

    def to_representation(self,instance,**kwargs) : 
        context = super().to_representation(instance,**kwargs)
        if hasattr(instance,"user") : 
            context["user"] = UserInfoSerializer(
                instance.user,
                context=self.context
            ).data
        return context


# افزودن چندین محصول

class MultipleProductOrderSerializer (serializers.Serializer) : 

    products_count = serializers.ListField(
        child = ProductCountSerializer()
    )