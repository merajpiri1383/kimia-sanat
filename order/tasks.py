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



# send sms to user for order has been paid 


body_id_send_user_for_paid_order = "265544"
@shared_task
def send_sms_to_user_for_paid_order_state (user_phone,order_tracking_ocde,order_number) : 
    try : 
        user = get_user_model().objects.get(phone=user_phone)
        sms.send_by_base_number(
            text=f"{user.username()};{order_tracking_ocde};{order_number}",
            bodyId=body_id_send_user_for_paid_order,
            to=user_phone,
        )
    except : 
        pass 


# reject order of user 

body_id_send_reject_order = "265541"

@shared_task
def send_sms_for_reject_order (user_phone,order_tracking_code) : 
    
    try :
        user = get_user_model().objects.get(user=user_phone)
        sms.send_by_base_number(
            text=f"{user.username};{order_tracking_code}",
            bodyId=body_id_send_reject_order,
            to=user_phone
        )
    except : 
        pass 