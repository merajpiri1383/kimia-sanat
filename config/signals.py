from django.dispatch import receiver
from django.db.models.signals import post_migrate
from config.models import AboutUs,ContactUs

@receiver(post_migrate)
def create_settings_instance(sender,**kwargs) : 
    
    if not AboutUs.objects.first() : 
        AboutUs.objects.create()

    if not ContactUs.objects.first() : 
        ContactUs.objects.create()