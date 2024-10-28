from utils.sms import sms
from celery import shared_task

body_id = "262233"


@shared_task
def send_admin_new_order (username,order_number,admin_phone) : 
    sms.send_by_base_number(
        text=f"{username};{order_number}",
        to=admin_phone,
        bodyId=body_id,
    )