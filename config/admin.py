from django.contrib import admin
from config.models import (OrderingGuide,Achievements,Feq,Story,ContactItem,SocialContact,AboutUs,ContactUs
                        ,ContactTitle,FeqTitle,OrderGuideTitle,SocialTitle,StoryItem,Location,ContactConsult)

from nested_inline.admin import NestedTabularInline,NestedModelAdmin,NestedStackedInline

# مدل درباره ما 

class StoryItemInline (NestedTabularInline) : 
    model = StoryItem
    exclude = ["id"]
    extra = 0

class StoryInline (NestedStackedInline) : 
    model = Story
    exclude = ["id"]
    extra = 0
    inlines = [StoryItemInline]

class AchievementsInline (admin.StackedInline) : 
    model = Achievements
    exclude = ["id"]
    extra = 0

class OrderGuideTitleInline (admin.StackedInline) : 
    model = OrderGuideTitle
    exclude = ["id"]
    extra = 0

class OrderingGuideInline (admin.TabularInline) : 
    model = OrderingGuide
    exclude = ["id"]
    extra = 0

class FeqTitleInline (admin.StackedInline) : 
    model = FeqTitle 
    exclude = ["id"]
    extra = 0

class FeqInline (admin.TabularInline) : 
    model = Feq
    exclude = ["id"]
    extra = 0


@admin.register(AboutUs)
class AboutUsAdmin (NestedModelAdmin) :
    exclude = ["id"]
    inlines = [StoryInline,AchievementsInline,OrderGuideTitleInline,OrderingGuideInline,FeqTitleInline,FeqInline]


# مدل ارتباط با ما

class ContactTitleInline (admin.StackedInline) : 
    model = ContactTitle
    extra = 0
    exclude = ["id"]

class ContactItemInline (admin.TabularInline) : 
    model = ContactItem
    extra = 0
    exclude = ["id"]

class SocialTitleInline (admin.StackedInline) : 
    model = SocialTitle
    extra = 0
    exclude = ["id"]

class SocialItemInline (admin.TabularInline) : 
    model = SocialContact
    extra = 0
    exclude = ["id"]

class LocationInline (admin.StackedInline) : 
    model = Location
    extra = 0
    exclude = ["id"]

@admin.register(ContactUs)
class ContactUsAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [ContactTitleInline,ContactItemInline,SocialTitleInline,SocialItemInline,LocationInline]


@admin.register(ContactConsult)
class ContactConsultAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    list_display = ["index","name","department","phone","email","text"]
    readonly_fields = ["index"]

    def index (self,obj )  : 
        return list(ContactConsult.objects.all()).index(obj) + 1
    index.short_description = "ردیف"