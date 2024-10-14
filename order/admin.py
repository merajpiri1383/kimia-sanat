from django.contrib import admin
from order.models import Order,PaySlip,Rule,PreInvoice,PreInvoiceProduct
from nested_inline.admin import NestedStackedInline,NestedModelAdmin,NestedTabularInline


class PreInvoiceProductInline (NestedTabularInline) : 
    model = PreInvoiceProduct
    extra = 0   
    exclude = ["id"]
    fields = ["title","count","unit","colleague_price","buy_price","totoal_price"]
    readonly_fields = ["colleague_price","buy_price","totoal_price"]

    

class PreInvoiceInline (NestedTabularInline) : 
    inlines = [PreInvoiceProductInline]
    model = PreInvoice
    extra = 0
    exclude = ["id"]


class PaySlipInline (NestedStackedInline) : 
    model = PaySlip
    extra = 0 
    exclude = ["id"]

@admin.register(Order)
class OrderAdmin (NestedModelAdmin) : 
    exclude = ["id"]
    inlines = [PaySlipInline,PreInvoiceInline]

@admin.register(Rule)
class RuleAdmin (admin.ModelAdmin) : 
    exclude = ["id"]