from django.contrib import admin
from project.models import Category,Project,ProjectImage,Comment,ProjectsPage,VideoProject,ViolationComment
from jalali_date.admin import ModelAdminJalaliMixin

# تصاویر پروژه
class ProjectImageInline(admin.TabularInline) :
    model = ProjectImage
    exclude = ["id"]
    extra = 0

# ویدیو های پروژه 
class VideoProjectInline (admin.TabularInline) : 
    model = VideoProject
    exclude = ["id"]
    extra = 0

# مدل دسته بندی
@admin.register(Category)
class CategoryAdminModel(admin.ModelAdmin) :
    exclude = ["id","slug"]

# مدل پروژه
@admin.register(Project)
class ProjectAdminModel(ModelAdminJalaliMixin,admin.ModelAdmin) :
    exclude = ["id","slug"]
    inlines = [ProjectImageInline,VideoProjectInline]

class ViolationCommentInline (admin.StackedInline) : 
    model = ViolationComment
    exclude = ["id"]
    extra = 0


# مدل کامنت
@admin.register(Comment)
class CommentAdmin (admin.ModelAdmin) :
    exclude = ["id"]
    search_fields = ["project","email","name",'description']
    list_filter = ["project","is_valid","created","reply_to"]
    inlines = [ViolationCommentInline]


# صفحه پروژه ها 
@admin.register(ProjectsPage)
class ProjectsPageAdmin (admin.ModelAdmin) : 
    exclude = ["id"]