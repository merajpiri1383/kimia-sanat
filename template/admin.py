from django.contrib import admin
from template.models import ( AchievementTitle,AnswerQuestionTitle,BlogTitle,CommingSoon,
        CommnetTemplate,ProductTitle,ProjectTitle,Menu,SubMenu,Template)


# مدل منو

class SubMenuTabular (admin.TabularInline) : 
    model = SubMenu
    extra = 1 
    exclude = ["id"]

@admin.register(Menu)
class MenuAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [SubMenuTabular]




# مدل قالب 

class ProjectTitleTabular (admin.TabularInline) : 
    model = ProjectTitle
    extra = 0
    exclude = ["id"]

class BlogTitleTabular (admin.TabularInline) : 
    model = BlogTitle
    extra = 0
    exclude = ["id"]

class CommingSoonTabular (admin.StackedInline) : 
    model = CommingSoon
    extra = 0
    exclude = ['id']

class ProductTitleTabular (admin.TabularInline) : 
    model = ProductTitle
    extra = 0 
    exclude = ["id"]

class AchievementTitleTabular (admin.TabularInline) : 
    model = AchievementTitle
    extra = 0
    exclude = ["id"]

class AnswerQuestionTitleTabular (admin.TabularInline) : 
    model = AnswerQuestionTitle 
    extra = 0
    exclude = ["id"]

@admin.register(Template)
class TemplateAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [ProjectTitleTabular,BlogTitleTabular,CommingSoonTabular,ProductTitleTabular,AchievementTitleTabular]


# مدل کامنت 
@admin.register(CommnetTemplate)
class CommentAdmin(admin.ModelAdmin) : 
    exclude = ["id"]