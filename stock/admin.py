from django.contrib import admin
from stock.models import ProductGroup
from product.models import Product,Count
from nested_inline.admin import NestedModelAdmin,NestedStackedInline,NestedTabularInline



class CountInline (NestedTabularInline) : 
    model = Count
    exclude = ["id"]
    extra = 0

class ProductInline (NestedStackedInline) : 
    model = Product
    exclude = ["id","liked","slug","views"]
    extra = 0
    inlines = [CountInline]

@admin.register(ProductGroup)
class ProductGroupAdmin (NestedModelAdmin) : 
    exclude = ["id"]
    inlines = [ProductInline]