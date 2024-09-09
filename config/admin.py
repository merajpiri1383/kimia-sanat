from django.contrib import admin
from config.models import Settings,OrderingGuide,Achievements,Feq,Story

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


@admin.register(Settings)
class SettingsModelAdmin(admin.ModelAdmin) :
    
    inlines = [StoryInline,FeqInline,OrderingGuideInline,AchievementInline]

# راهنمای سفارش
@admin.register(OrderingGuide)
class OrderingGuideModelAdmin(admin.ModelAdmin) : 
    exclude = ["id","settings"]

# سوالات متداول
@admin.register(Feq)
class FeqModelAdmin(admin.ModelAdmin) : 
    exclude = ["id","settings"]
