from django.contrib import admin
from product.models import (Product,Category,UsageProduct,FeatureProduct,Standard
            ,ImageProduct,Comment,ViolationComment)
from django.db import models 
from django_summernote.admin import SummernoteWidget
from nested_inline.admin import NestedModelAdmin,NestedStackedInline
from django.utils.html import format_html

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


# مدل محصول
@admin.register(Product)
class ProductAdmin (admin.ModelAdmin) :
    exclude = ["id","slug","views","liked","group","count"]
    inlines = [UsageProductStackInline,FeatureProductStackInline,ImageProductInline]
    list_display = ["index","title","category","code","type"]
    readonly_fields = ["index"]
    formfield_overrides = {
        models.TextField : { 'widget' : SummernoteWidget }
    }

# مدل استاندارد
@admin.register(Standard)
class StandardAdmin (admin.ModelAdmin) :
    exclude = ["id"]
    list_display = ["index","show_image","name","text"]
    readonly_fields = ["index","show_image"]

    def index (self,obj) : 
        return list(Standard.objects.all()).index(obj) + 1 
    index.short_description = "ردیف"

    def show_image (self,obj) : 
        if obj.image:  # بررسی وجود تصویر
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "بدون تصویر"
    show_image.short_description = "تصویر"


# مدل دسته بندی
@admin.register(Category)
class CategoryAdmin ( admin.ModelAdmin ) :
    exclude = ["id","slug"]

class ViolationCommentInline (NestedStackedInline) : 
    model = ViolationComment
    exclude = ["id"]
    extra = 0



class CommentInline (NestedStackedInline) : 
    model = Comment
    exclude = ["id"]
    extra = 0

    
# مدل کامنت
@admin.register(Comment)
class CommentAdmin (NestedModelAdmin) :
    exclude = ["id"]
    search_fields = ["product","email","name",'description']
    list_filter = ["product","is_valid","created","reply_to"]
    inlines = [ViolationCommentInline,CommentInline]
    list_display = ["index","name","get_product","reply_count"]
    readonly_fields = ["index","get_product","reply_count"]

    def index (self,obj) : 
        return list(Comment.objects.all()).index(obj) + 1
    index.short_description = "ردیف"

    def reply_count (self,obj) : 
        return obj.replys.count()
    reply_count.short_description = "تعداد پاسخ ها"

    def get_product (self,obj) : 
        return obj.product.title
    get_product.short_description = "محصول"