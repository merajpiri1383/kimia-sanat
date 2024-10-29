from django.contrib import admin
from template.main.models import (
    Achievement,
    AchievementCard,
    AchievementCardItem,
    AchievementTitle,
    AnswerQuestionTitle,
    BlogTitle,
    Comment,
    Consult,
    FirstPageContent,
    PhoneAnswerQuestion,
    ProductTitle,
    ProjectTitle,
    Slider,
)


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

# درخواست های مشاوره
@admin.register(Consult)
class ConsultAdmin (admin.ModelAdmin) : 
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