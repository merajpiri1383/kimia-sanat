from django.contrib import admin
from notification.models import Notification,NotificationPage


@admin.register(NotificationPage)
class NotificationPageAdmin (admin.ModelAdmin) : 
    exclude = ["id"]


@admin.register(Notification) 
class NotificationAdmin (admin.ModelAdmin) : 
    exclude = ["id","created","read_users"]
    list_display = ["title","send_to_all","created"]