from django.contrib import admin
from template.models import ( AchievementCard,Comment,BlogTitle,CommingSoon
                            ,ProductTitle,ProjectTitle,Menu,SubMenu,AnswerQuestionTitle,CategoryFooter,
                            Header,Slider,ImageSlider,FirstPageContent,License,Footer,FooterLink,PhoneFooter,SocialFooter
                            ,AchievementCardItem)

from nested_inline.admin import NestedStackedInline, NestedModelAdmin,NestedTabularInline

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

class SubMenuTabular (NestedTabularInline) : 
    model = SubMenu
    extra = 0
    exclude = ["id"]
    fk_name = "menu"

class MenuInline (NestedStackedInline) : 
    exclude = ["id"]
    model = Menu
    extra = 0
    fk_name = 'header'
    inlines = [SubMenuTabular]

@admin.register(Header) 
class HeaderAdmin (NestedModelAdmin) : 
    exclude = ["id"]
    inlines = [MenuInline]

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
class AchievementCardItemInline (admin.TabularInline) : 
    model = AchievementCardItem
    extra = 0
    exclude = ["id"]

@admin.register(AchievementCard)
class AchievementTitleAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [AchievementCardItemInline]

# فوتر 

class FooterLinkInline (admin.TabularInline) : 
    model = FooterLink
    extra = 0 
    exclude = ["id"]

class SocialFooterInline (admin.TabularInline) : 
    model = SocialFooter
    extra = 0
    exclude = ["id"]

class PhoneFooterInline (admin.TabularInline) : 
    model = PhoneFooter
    exclude = ["id"]
    extra = 0

class CategoryFooterInline (admin.TabularInline) : 
    model = CategoryFooter
    exclude = ["id"]
    extra = 0

@admin.register(Footer)
class FooterAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines= [FooterLinkInline,SocialFooterInline,PhoneFooterInline,CategoryFooterInline]