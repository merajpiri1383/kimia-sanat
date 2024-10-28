from celery import shared_task
from utils.sms import sms



body_id_ticket_is_responsed = "262240"
@shared_task
def send_user_ticket_responsed (name,phone,ticket_number) : 
    sms.send_by_base_number(
        text=f"{name};{ticket_number}",
        to=phone,
        bodyId=body_id_ticket_is_responsed
    )


body_id_ticket_is_sent = "262237"
@shared_task
def send_user_ticket_is_sent (name,phone,ticket_number ) : 
    sms.send_by_base_number(
        text=f"{name};{ticket_number}",
        to=phone,
        bodyId=body_id_ticket_is_sent
    )



body_id_send_admin = "262235"
@shared_task
def send_admin_user_send_ticket (username,ticket_number,admin_phone) : 
    sms.send_by_base_number(
        text=f"{username};{ticket_number}",
        to=admin_phone,
        bodyId=body_id_send_admin
    )