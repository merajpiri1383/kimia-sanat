from django.contrib import admin
from order.models import Order,PaySlip,Rule,PreInvoice,PreInvoiceProduct,ProductCount
from nested_inline.admin import NestedStackedInline,NestedModelAdmin,NestedTabularInline
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.html import format_html


class PreInvoiceProductInline (NestedTabularInline) : 
    model = PreInvoiceProduct
    extra = 0   
    exclude = ["id"]
    fields = ["title","count","unit","colleague_price","buy_price","totoal_price"]
    readonly_fields = ["colleague_price","buy_price","totoal_price"]

    

class PreInvoiceInline (NestedStackedInline) : 
    inlines = [PreInvoiceProductInline]
    model = PreInvoice
    extra = 0
    fields = ["get_total","is_for_collegue","is_for_customer","is_final","description"]
    readonly_fields = ["get_total"]

    def get_total(self,obj) : 
        return format_html(f"<b>{intcomma(obj.total_price,False)}</b>")
    
    get_total.short_description = "قیمت کل (ریال)"


class PaySlipInline (NestedStackedInline) : 
    model = PaySlip
    extra = 0 
    exclude = ["id"]

class ProductCountInline (NestedTabularInline) : 
    model = ProductCount
    exclude = ["id"]
    extra = 0

@admin.register(Order)
class OrderAdmin (NestedModelAdmin) : 
    exclude = ["id"]
    list_display = ["index","get_user_name","get_phone","tracking_code","state"]
    inlines = [PaySlipInline,PreInvoiceInline,ProductCountInline]

    def index (self,obj) : 
        return list(Order.objects.all().order_by("-created")).index(obj) + 1 
    index.short_description = "ردیف"
    
    def get_user_name (self,obj) : 
        if hasattr(obj.user,"real_profile") : 
            return obj.user.real_profile.name
        elif hasattr(obj.user,"legal_profile") : 
            return obj.user.legal_profile.name 
    get_user_name.short_description = "نام کاربر"

    def get_phone(self,obj) : 
        return obj.user.phone
    get_phone.short_description = "شماره موبایل"



@admin.register(Rule)
class RuleAdmin (admin.ModelAdmin) : 
    exclude = ["id"]