from django.contrib import admin
from project.models import Category,Project,ProjectImage,Comment,ProjectsPage,VideoProject,ViolationComment
from jalali_date.admin import ModelAdminJalaliMixin
from nested_inline.admin import NestedModelAdmin,NestedStackedInline,NestedTabularInline
from django.utils.html import format_html

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
    list_display = ["index","get_cover","name"]

    def index (self,obj) : 
        return list(Category.objects.all()).index(obj) + 1
    index.short_description = 'ردیف'

    def get_cover (self,obj) : 
        return format_html("<img src='{}' height='50' width='50' />",obj.cover.url)
    get_cover.short_description = "کاور"

# مدل پروژه
@admin.register(Project)
class ProjectAdminModel(ModelAdminJalaliMixin,admin.ModelAdmin) :
    exclude = ["id","slug"]
    inlines = [ProjectImageInline,VideoProjectInline]
    list_display = ["index","name","get_category","contractor","start_date","launch_date"]
    

    def index(self,obj) : 
        return list(Project.objects.all()).index(obj) + 1
    index.short_description = "ردیف"

    def get_category (self,obj) : 
        if obj.category : 
            return obj.category.name
    get_category.short_description = "دسته بندی"

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
    list_display = ["index","name","get_project","replys_count"]
    readonly_fields = ["index","get_project","replys_count"]

    def index (self,obj) : 
        return list(Comment.objects.all()).index(obj) + 1
    index.short_description = "ردیف"

    def get_project (self,obj) : 
        return obj.project.name
    get_project.short_description = "پروژه"

    def replys_count (self,obj) : 
        return obj.replys.count()
    replys_count.short_description = "تعداد پاسخ ها"


# صفحه پروژه ها 
@admin.register(ProjectsPage)
class ProjectsPageAdmin (admin.ModelAdmin) : 
    exclude = ["id"]