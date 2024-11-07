from utils.sms import sms
from celery import shared_task
from order.models import Order,PreInvoice
from django.contrib.auth import get_user_model

body_id = "265537"


@shared_task
def send_admin_new_order (username,order_number,admin_phone) : 
    sms.send_by_base_number(
        text=f"{username};{order_number}",
        to=admin_phone,
        bodyId=body_id,
)
    
@shared_task
def send_sms_to_admin_for_creating_order (order_id) : 
    
    try : 
        order = Order.objects.get(id=order_id)
        PreInvoice.objects.create(order=order)
        for user in get_user_model().objects.filter(send_sms=True,is_staff=True) : 
                send_admin_new_order.apply_async(args=[
                    order.user.username(),
                    order.tracking_code,
                    user.phone
            ])
    except : 
        pass 



body_id_send_pay_slip_by_user = "265547"
@shared_task
def send_pay_slip_by_user_sms (pre_pay_slip_number,username) :
    try : 
        for user in get_user_model().objects.filter(is_staff=True,send_sms=True) : 
            sms.send_by_base_number(
                text=f"{pre_pay_slip_number};{username}",
                bodyId=body_id_send_pay_slip_by_user,
                to=user.phone
            )
    except : pass 