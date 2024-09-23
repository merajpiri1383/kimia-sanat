from django.contrib import admin
from project.models import Category,Project,ProjectImage,Comment,ProjectsPage

# تصاویر پروژه
class ProjectImageInline(admin.TabularInline) :
    model = ProjectImage
    exclude = ["id"]
    extra = 1

# مدل دسته بندی
@admin.register(Category)
class CategoryAdminModel(admin.ModelAdmin) :
    exclude = ["id","slug"]

# مدل پروژه
@admin.register(Project)
class ProjectAdminModel(admin.ModelAdmin) :
    exclude = ["id","slug"]
    inlines = [ProjectImageInline]


# مدل کامنت
@admin.register(Comment)
class CommentAdmin (admin.ModelAdmin) :
    exclude = ["id"]
    search_fields = ["project","email","name",'description']
    list_filter = ["project","is_valid","created","reply_to"]


# صفحه پروژه ها 
@admin.register(ProjectsPage)
class ProjectsPageAdmin (admin.ModelAdmin) : 
    exclude = ["id"]