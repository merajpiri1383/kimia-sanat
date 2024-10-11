from django.contrib import admin
from project.models import Category,Project,ProjectImage,Comment,ProjectsPage,VideoProject,ViolationComment
from jalali_date.admin import ModelAdminJalaliMixin
from nested_inline.admin import NestedModelAdmin,NestedStackedInline

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

class ViolationCommentInline (NestedStackedInline) : 
    model = ViolationComment
    exclude = ["id"]
    extra = 0

class CommentInline (NestedStackedInline) : 
    model = Comment
    extra = 0
    exclude = ["id"]


# مدل کامنت
@admin.register(Comment)
class CommentAdmin (NestedModelAdmin) :
    exclude = ["id"]
    search_fields = ["project","email","name",'description']
    list_filter = ["project","is_valid","created","reply_to"]
    inlines = [ViolationCommentInline,CommentInline]


# صفحه پروژه ها 
@admin.register(ProjectsPage)
class ProjectsPageAdmin (admin.ModelAdmin) : 
    exclude = ["id"]