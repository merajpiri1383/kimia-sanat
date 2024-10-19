from django.contrib import admin
from notification.models import Notification,NotificationPage


@admin.register(NotificationPage)
class NotificationPageAdmin (admin.ModelAdmin) : 
    exclude = ["id"]


@admin.register(Notification) 
class NotificationAdmin (admin.ModelAdmin) : 
    exclude = ["id","created","read_users"]
    list_display = ["index","title","send_to","created"]
    readonly_fields = ["index","send_to"]

    def index (self,obj) : 
        return list(Notification.objects.all()).index(obj) + 1
    index.short_description = "ردیف"
    
    def send_to (self,obj) : 
        if obj.send_to_all : 
            return "همه"
        elif obj.user : 
            return obj.user
    send_to.short_description = 'ارسال به '
    