from django.dispatch import receiver
from django.db.models.signals import post_save
from order.models import Order,PreInvoice
from django.contrib.auth import get_user_model
from order.tasks import send_sms_to_admin_for_creating_order

@receiver(signal=post_save,sender=Order)
def create_pre_invoice (sender,instance,created,**kwargs) : 
    if created : 
        send_sms_to_admin_for_creating_order.apply_async(args=[instance.id])