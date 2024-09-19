from django.contrib import admin
from profuser.models import Driver

@admin.register(Driver)
class DriverAdmin (admin.ModelAdmin) : 
    exclude = ["id"]