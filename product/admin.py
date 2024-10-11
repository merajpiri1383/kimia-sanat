from django.contrib import admin
from product.models import (Product,Category,UsageProduct,FeatureProduct,Standard,Count
            ,ImageProduct,Comment,ViolationComment)
from django.db import models 
from django_summernote.admin import SummernoteWidget

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
    exclude = ["id","slug","views","liked"]
    inlines = [UsageProductStackInline,FeatureProductStackInline,ImageProductInline,CountInline]
    formfield_overrides = {
        models.TextField : { 'widget' : SummernoteWidget }
    }

# مدل استاندارد
@admin.register(Standard)
class StandardAdmin (admin.ModelAdmin) :
    exclude = ["id"]


# مدل دسته بندی
@admin.register(Category)
class CategoryAdmin ( admin.ModelAdmin ) :
    exclude = ["id","slug"]

class ViolationCommentInline (admin.StackedInline) : 
    model = ViolationComment
    exclude = ["id"]
    extra = 0

# مدل کامنت
@admin.register(Comment)
class CommentAdmin (admin.ModelAdmin) :
    exclude = ["id"]
    search_fields = ["product","email","name",'description']
    list_filter = ["product","is_valid","created","reply_to"]
    inlines = [ViolationCommentInline]