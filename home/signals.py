from django.dispatch import receiver
from django.db.models.signals import post_migrate
from home.models import Company


@receiver(post_migrate)
def create_company (sender,**kwargs) : 

    company = Company.objects.first()

    if not company : 
        Company.objects.create()