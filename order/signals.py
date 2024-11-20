from django.dispatch import receiver
from django.db.models.signals import post_save
from order.models import Order,PaySlip
from order.tasks import (
    send_sms_to_admin_for_creating_order,
    send_pay_slip_by_user_sms,
    send_sms_to_user_for_paid_order_state,
    send_sms_for_reject_order
)

@receiver(signal=post_save,sender=Order)
def create_pre_invoice (sender,instance,created,**kwargs) : 
    if created : 
        send_sms_to_admin_for_creating_order.apply_async(args=[instance.id])
    if instance.state == "paid" : 
        send_sms_to_user_for_paid_order_state.apply_async(args=[
            instance.user.phone,
            instance.tracking_code,
            instance.tracking_code,
        ])
    if instance.state == "reject" : 
        send_sms_for_reject_order.apply_async(args=[
            instance.user.phone,
            instance.tracking_code,
        ])



@receiver(signal=post_save,sender=PaySlip)
def send_sms_to_admin_for_payslip (sender,instance,created,**kwargs) : 
    if created : 
        send_pay_slip_by_user_sms.apply_async(args=[
            instance.order.tracking_code,
            instance.order.user.phone,
        ])