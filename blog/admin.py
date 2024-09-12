from django.contrib import admin
from blog.models import Blog,Category,Module

class ModuleStackInline (admin.StackedInline) :

    model = Module
    extra = 1
    exclude = ["id"]

# مدل دسته بندی
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin) :
    exclude = ["id","slug"]


# مدل بلاگ
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin) :
    inlines = [ModuleStackInline]
    exclude = ["id","slug"]