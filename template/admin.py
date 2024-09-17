from django.contrib import admin
from template.models import ( AchievementTitle,Comment,BlogTitle,CommingSoon
                            ,ProductTitle,ProjectTitle,Menu,SubMenu,AnswerQuestionTitle,
                            Header,Slider,ImageSlider,FirstPageContent,License)


# عنوان پروژه 

class CommentInline (admin.StackedInline) : 
    model = Comment
    exclude = ["id"]
    extra = 1

@admin.register(ProjectTitle)
class ProjectTitleAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [CommentInline]

# مدل بلاگ
@admin.register(BlogTitle)
class BlogTitleAdmin (admin.ModelAdmin) : 
    exclude = ["id"]


# مدل منو

class SubMenuTabular (admin.TabularInline) : 
    model = SubMenu
    extra = 1 
    exclude = ["id"]

@admin.register(Menu)
class MenuAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [SubMenuTabular]


# مدیرت محتوای صفحه اول
class LicenseInline (admin.StackedInline) : 
    exclude = ["id"]
    model = License
    extra = 1

@admin.register(FirstPageContent) 
class FirstPageContentAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [LicenseInline]

# اسلایدر

class SliderTabular (admin.TabularInline) : 
    model = ImageSlider
    exclude = ["id"]
    extra = 1

@admin.register(Slider)
class SliderAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [SliderTabular]


# مدل هدر 
@admin.register(Header)
class HeaderAdmin (admin.ModelAdmin) : 
    exclude = ["id"]

# مدیرت Comming Soon
@admin.register(CommingSoon) 
class CommingSoonAdminModel (admin.ModelAdmin) : 
    exclude = ["id"]


# عنوان محصولات و زیر عنوان 
@admin.register(ProductTitle)
class ProductTitleAdmin (admin.ModelAdmin) : 
    exclude = ["id"]


# مدیرت سوالات شما 

@admin.register(AnswerQuestionTitle)
class AnswerQuestionTitleAdmin (admin.ModelAdmin) : 
    exclude = ['id']

# مدیرت عنوان دستاورد ها
@admin.register(AchievementTitle)
class AchievementTitleAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
