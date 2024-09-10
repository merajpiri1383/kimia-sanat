from django.contrib import admin
from config.models import Settings,OrderingGuide,Achievements,Feq,Story,ContactItem,SocialContact

class StoryInline(admin.StackedInline) :
    model = Story
    extra = 0
    exclude = ["id"]

class OrderingGuideInline(admin.StackedInline) : 
    model = OrderingGuide
    extra = 1
    exclude = ["id"]

class AchievementInline(admin.StackedInline) : 
    model = Achievements
    extra = 1
    exclude = ["id"]

class FeqInline(admin.StackedInline) : 
    model = Feq
    extra = 1
    exclude = ["id"]

class SocialInline(admin.StackedInline) : 
    model = SocialContact
    extra = 1
    exclude = ["id"]

class ContactItemInline(admin.StackedInline) : 
    model = ContactItem
    extra = 1
    exclude = ["id"]


@admin.register(Settings)
class SettingsModelAdmin(admin.ModelAdmin) :
    
    inlines = [StoryInline,FeqInline,OrderingGuideInline,AchievementInline,SocialInline,ContactItemInline]

# راهنمای سفارش
@admin.register(OrderingGuide)
class OrderingGuideModelAdmin(admin.ModelAdmin) : 
    exclude = ["id","settings"]

# سوالات متداول
@admin.register(Feq)
class FeqModelAdmin(admin.ModelAdmin) : 
    exclude = ["id","settings"]

# راه های ارتباطی
@admin.register(ContactItem)
class ContactAdminModel(admin.ModelAdmin) : 
    exclude = ["id","settings"]

# شبکه های اجتماعی
@admin.register(SocialContact) 
class SocialAdminModel(admin.ModelAdmin) : 
    exclude = ["id","settings"]