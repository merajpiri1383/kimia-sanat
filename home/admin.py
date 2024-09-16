from django.contrib import admin
from home.models import Slider,Consult,ImageSlider,License


# مدل مشاوره 
@admin.register(Consult)
class ConsultAdmin (admin.ModelAdmin) : 
    exclude = ["id"]

# تصاویر سالایدر صفحه هوم
class  ImageSliderTabular (admin.TabularInline) : 
    model = ImageSlider
    extra = 1 
    exclude = ["id"]

# مدل شرکت
@admin.register(Slider)
class SliderAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [ImageSliderTabular]


# مدل گواهی نامه ها
@admin.register(License)
class LicenseAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    search_fields = ["title","description"]