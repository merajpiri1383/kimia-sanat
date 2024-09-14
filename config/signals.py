from django.dispatch import receiver
from django.db.models.signals import post_migrate
from config.models import Settings

@receiver(post_migrate)
def create_settings_instance(sender,**kwargs) : 
    setting = Settings.objects.get_or_create(pk=1)