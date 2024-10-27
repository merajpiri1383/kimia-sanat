from django.contrib import admin
from driver.models import Driver,DriverListPage

@admin.register(Driver)
class DriverAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    list_display = ["index","name","phone","national_id"]
    ordering = ["-created"]

    def index (self,obj) : 
        return list(Driver.objects.all()).index(obj) + 1
    index.short_description = "ردیف"


@admin.register(DriverListPage)
class DriverListPageAdmin (admin.ModelAdmin) : 
    exclude = ["id"]