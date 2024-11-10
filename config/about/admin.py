from django.contrib import admin
from config.models import (
    OrderingGuide,
    Achievements,
    Feq,Story,
    AboutUs,
    FeqTitle,
    OrderGuideTitle,
    StoryItem
)

from nested_inline.admin import (
    NestedTabularInline,
    NestedModelAdmin,
    NestedStackedInline)

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

class OrderingGuideInline (admin.StackedInline) : 
    model = OrderingGuide
    exclude = ["id"]
    extra = 0

class FeqTitleInline (admin.StackedInline) : 
    model = FeqTitle 
    exclude = ["id"]
    extra = 0

class FeqInline (admin.StackedInline) : 
    model = Feq
    exclude = ["id"]
    extra = 0


@admin.register(AboutUs)
class AboutUsAdmin (NestedModelAdmin) :
    exclude = ["id"]
    inlines = [StoryInline,AchievementsInline,OrderGuideTitleInline,OrderingGuideInline,FeqTitleInline,FeqInline]