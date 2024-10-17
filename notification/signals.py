from django.dispatch import receiver
from django.db.models.signals import post_migrate
from notification.models import NotificationPage


@receiver(post_migrate)
def create_notification_page(sender,**kwargs) : 

    if not NotificationPage.objects.first() : 
        NotificationPage.objects.create()