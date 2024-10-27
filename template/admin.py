from django.contrib import admin
from template.models import ( AchievementCard,Comment,BlogTitle,CommingSoon
                            ,ProductTitle,ProjectTitle,Menu,SubMenu,AnswerQuestionTitle,CategoryFooter,
                            Header,FirstPageContent,Footer,FooterLink,PhoneFooter
                            ,AchievementCardItem,Consult,ElectroLicense,CustomerClub,Slider,
                            PhoneAnswerQuestion,AchievementTitle,Achievement,FooterFeq,)

from nested_inline.admin import NestedStackedInline, NestedModelAdmin,NestedTabularInline
from jalali_date.admin import ModelAdminJalaliMixin

from template.panel.admin import *

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



@admin.register(FirstPageContent) 
class FirstPageContentAdmin (admin.ModelAdmin) : 
    exclude = ["id"]

# اسلایدر


@admin.register(Slider)
class SliderAdmin (admin.ModelAdmin) : 
    exclude = ["id"]


# مدل هدر 

class SubMenuTabular (NestedStackedInline) : 
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
class CommingSoonAdminModel (ModelAdminJalaliMixin,admin.ModelAdmin) : 
    exclude = ["id"]


# عنوان محصولات و زیر عنوان 
@admin.register(ProductTitle)
class ProductTitleAdmin (admin.ModelAdmin) : 
    exclude = ["id"]


# مدیرت سوالات شما  

class PhoneInline (admin.TabularInline) : 
    model = PhoneAnswerQuestion
    extra = 0
    exclude = ["id"]

@admin.register(AnswerQuestionTitle)
class AnswerQuestionTitleAdmin (admin.ModelAdmin) : 
    exclude = ['id']
    inlines = [PhoneInline]

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


class PhoneFooterInline (admin.TabularInline) : 
    model = PhoneFooter
    exclude = ["id"]
    extra = 0

class CategoryFooterInline (admin.TabularInline) : 
    model = CategoryFooter
    exclude = ["id"]
    extra = 0

class ElectroLicenseInline (admin.TabularInline) : 
    model = ElectroLicense
    exclude = ["id"]
    extra = 0

class FooterFeqInline (admin.StackedInline) : 
    model = FooterFeq
    exclude = ["id"]
    extra = 0

@admin.register(Footer)
class FooterAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines= [
        FooterLinkInline,
        PhoneFooterInline,
        CategoryFooterInline,
        ElectroLicenseInline,
        FooterFeqInline
    ]


# درخواست های مشاوره
@admin.register(Consult)
class ConsultAdmin (admin.ModelAdmin) : 
    exclude = ["id"]


# باشگاه مشتریان
@admin.register(CustomerClub)
class CustomerClubAdmin (admin.ModelAdmin) : 
    exclude = ["id"]


# دستاورد ها

class AchievementInline (admin.StackedInline) : 
    model = Achievement
    exclude = ["id"]
    extra = 0

@admin.register(AchievementTitle)
class AchievementTitleAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [AchievementInline]


