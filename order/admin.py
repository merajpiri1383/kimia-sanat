from django.contrib import admin
from order.models import Order,PaySlip,Rule


class PaySlipInline (admin.StackedInline) : 
    model = PaySlip
    extra = 0 
    exclude = ["id"]

@admin.register(Order)
class OrderAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [PaySlipInline]

@admin.register(Rule)
class RuleAdmin (admin.ModelAdmin) : 
    exclude = ["id"]