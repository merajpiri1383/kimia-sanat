from django.contrib import admin
from project.models import Category,Project,ProjectImage

# تصاویر پروژه
class ProjectImageInline(admin.TabularInline) :
    model = ProjectImage
    exclude = ["id"]
    extra = 1

# مدل دسته بندی
@admin.register(Category)
class CategoryAdminModel(admin.ModelAdmin) :
    exclude = ["id"]

# مدل پروژه
@admin.register(Project)
class ProjectAdminModel(admin.ModelAdmin) :
    exclude = ["id"]
    inlines = [ProjectImageInline]