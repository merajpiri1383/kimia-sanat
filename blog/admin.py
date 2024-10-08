from django.contrib import admin
from blog.models import Blog,Category,Module,Comment,Tag
from django_summernote.widgets import SummernoteWidget
from django.db import models
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin	

class ModuleStackInline (StackedInlineJalaliMixin,admin.StackedInline) :

    model = Module
    extra = 0
    exclude = ["id"]
    formfield_overrides = {
        models.TextField : {'widget' : SummernoteWidget}
    }

# مدل دسته بندی
@admin.register(Category)
class CategoryAdmin(ModelAdminJalaliMixin,admin.ModelAdmin) :
    exclude = ["id","slug"]


# مدل بلاگ
@admin.register(Blog)
class BlogAdmin(ModelAdminJalaliMixin,admin.ModelAdmin) :
    inlines = [ModuleStackInline]
    exclude = ["id","slug"]
    list_filter = ["is_published","created_date","author"]
    search_fields = ["title","author","description"]


# مدل کامنت
@admin.register(Comment)
class CommentAdmin (ModelAdminJalaliMixin,admin.ModelAdmin) :
    exclude = ["id"]
    search_fields = ["blog","email","name",'description']
    list_filter = ["blog","is_valid","created","reply_to"]



# مدل برچسب
@admin.register(Tag)
class TagAdmin (admin.ModelAdmin) : 
    exclude = ["id","slug"]