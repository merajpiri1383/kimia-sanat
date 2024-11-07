from django.dispatch import receiver
from django.db.models.signals import post_save
from order.models import Order,PreInvoice,PaySlip
from django.contrib.auth import get_user_model
from order.tasks import (
    send_sms_to_admin_for_creating_order,
    send_pay_slip_by_user_sms
)

@receiver(signal=post_save,sender=Order)
def create_pre_invoice (sender,instance,created,**kwargs) : 
    if created : 
        send_sms_to_admin_for_creating_order.apply_async(args=[instance.id])



@receiver(signal=post_save,sender=PaySlip)
def send_sms_to_admin_for_payslip (sender,instance,created,**kwargs) : 
    if created : 
        send_pay_slip_by_user_sms.apply_async(args=[
            instance.order.tracking_code,
            instance.order.user.phone,
        ])