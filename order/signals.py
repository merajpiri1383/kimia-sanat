from django.dispatch import receiver
from django.db.models.signals import post_save
from order.models import Order,PreInvoice

@receiver(signal=post_save,sender=Order)
def create_pre_invoice (sender,instance,created,**kwargs) : 
    if created : 
        PreInvoice.objects.create(
            order = instance
        )