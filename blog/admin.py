from django.contrib import admin
from blog.models import Blog,Category,Module,Comment,Tag,ViolationComment
from django_summernote.widgets import SummernoteWidget
from django.db import models
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin
from nested_inline.admin import NestedModelAdmin,NestedStackedInline
from django.utils.html import format_html


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
    list_display = ["index","name","count_of_blogs"]

    def index (self,obj) : 
        return list(Category.objects.all()).index(obj) + 1 
    index.short_description = "ردیف"

    def count_of_blogs (self,obj) : 
        return obj.blogs.count()
    count_of_blogs.short_description = 'تعداد بلاگ ها'


# مدل بلاگ
@admin.register(Blog)
class BlogAdmin(ModelAdminJalaliMixin,admin.ModelAdmin) :
    inlines = [ModuleStackInline]
    exclude = ["id","slug"]
    list_filter = ["is_published","created_date","author"]
    search_fields = ["title","author","description"]
    list_display = ["index","get_image","title","author"]
    readonly_fields = ["index","get_image"]

    def index (self,obj) : 
        return list(Blog.objects.all()).index(obj) + 1
    index.short_description = "ردیف"

    def get_image (self,obj) : 
        return format_html("<img src='{}' height='50' width='50' />",obj.cover.url)
    get_image.short_description = "کاور"



class ViolationCommentInline (NestedStackedInline) : 
    model = ViolationComment
    exclude = ["id"]
    extra = 0

class CommentInline (NestedStackedInline) : 
    model = Comment
    exclude = ['id']
    extra = 0

# مدل کامنت
@admin.register(Comment)
class CommentAdmin (ModelAdminJalaliMixin,NestedModelAdmin) :
    exclude = ["id"]
    search_fields = ["blog","email","name",'description']
    list_filter = ["blog","is_valid","created","reply_to"]
    inlines = [ViolationCommentInline,CommentInline]
    list_display = ["index","name","blog_name","reply_count"]
    readonly_fields = ["index","reply_count","blog_name"]


    def index (self,obj) : 
        return list(Comment.objects.all()).index(obj) + 1
    index.short_description = "ردیف"

    def reply_count (self,obj) : 
        return obj.replys.count()
    reply_count.short_description = "تعداد پاسخ ها"

    def blog_name (self,obj) : 
        return obj.blog.title
    blog_name.short_description = "بلاگ"



# مدل برچسب
@admin.register(Tag)
class TagAdmin (admin.ModelAdmin) : 
    exclude = ["id","slug"]
