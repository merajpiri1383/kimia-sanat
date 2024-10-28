from django.dispatch import receiver
from django.db.models.signals import post_save
from order.models import Order,PreInvoice
from django.contrib.auth import get_user_model
from order.tasks import send_admin_new_order

@receiver(signal=post_save,sender=Order)
def create_pre_invoice (sender,instance,created,**kwargs) : 
    if created : 
        PreInvoice.objects.create(
            order = instance
        )
        try :
            for user in get_user_model().objects.filter(send_sms=True,is_staff=True) : 
                send_admin_new_order.apply_async(args=[
                    instance.user.username(),
                    instance.tracking_code,
                    user.phone
                ])
        except : 
            pass