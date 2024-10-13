from django.contrib import admin
from order.models import Order,PaySlip,Rule,PreInvoice,PreInvoiceProduct
from nested_inline.admin import NestedStackedInline,NestedModelAdmin,NestedTabularInline


class PreInvoiceProductInline (NestedStackedInline) : 
    model = PreInvoiceProduct
    extra = 0
    exclude = ["id"]

class PreInvoiceInline (NestedStackedInline) : 
    model = PreInvoice
    extra = 0
    exclude = ['id']
    inlines = [PreInvoiceProductInline]


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