from django.contrib import admin
from driver.models import Driver

@admin.register(Driver)
class DriverAdmin (admin.ModelAdmin) : 
    exclude = ["id"]