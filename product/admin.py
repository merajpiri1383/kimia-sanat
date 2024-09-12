from django.contrib import admin
from product.models import Product,Category,UsageProduct,FeatureProduct,Standard

# مدل کاربرد محصول
class UsageProductStackInline (admin.TabularInline) :
    model = UsageProduct
    extra = 1
    exclude = ["id"]

# مدل مشخصات محصول
class FeatureProductStackInline (admin.TabularInline) :
    model = FeatureProduct
    extra = 1
    exclude = ["id"]

# مدل محصول
@admin.register(Product)
class ProductAdmin (admin.ModelAdmin) :
    exclude = ["id"]
    inlines = [UsageProductStackInline,FeatureProductStackInline]

# مدل استاندارد
@admin.register(Standard)
class StandardAdmin (admin.ModelAdmin) :
    exclude = ["id"]


# مدل دسته بندی
@admin.register(Category)
class CategoryAdmin ( admin.ModelAdmin ) :
    exclude = ["id","slug"]