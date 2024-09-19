from django.contrib import admin
from product.models import (Product,Category,UsageProduct,FeatureProduct,Standard,Count
            ,ImageProduct,Tag,Comment)

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

# مدل تصویر محصول
class ImageProductInline (admin.TabularInline) :
    model = ImageProduct
    extra = 1
    exclude = ["id"]

class CountInline (admin.TabularInline) : 
    model = Count
    extra = 1 
    exclude = ["id"]

# مدل محصول
@admin.register(Product)
class ProductAdmin (admin.ModelAdmin) :
    exclude = ["id","slug","views"]
    inlines = [UsageProductStackInline,FeatureProductStackInline,ImageProductInline,CountInline]

# مدل استاندارد
@admin.register(Standard)
class StandardAdmin (admin.ModelAdmin) :
    exclude = ["id"]


# مدل دسته بندی
@admin.register(Category)
class CategoryAdmin ( admin.ModelAdmin ) :
    exclude = ["id","slug"]

# مدل برچسب
@admin.register(Tag)
class TagAdmin (admin.ModelAdmin) :
    exclude = ['id','slug']


# مدل کامنت
@admin.register(Comment)
class CommentAdmin (admin.ModelAdmin) :
    exclude = ["id"]
    search_fields = ["product","email","name",'description']
    list_filter = ["product","is_valid","created","reply_to"]