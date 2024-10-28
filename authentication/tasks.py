from celery import shared_task
from django.contrib.auth import get_user_model
from time import sleep
from utils.sms import sms


body_id = "260311"
def send_sms (phone,otp) : 
    sms.send_by_base_number(
        otp,
        phone,
        body_id
    )


@shared_task
def send_otp (phone) : 
    user = get_user_model().objects.get(phone=phone)
    send_sms(user.phone,user.otp_code)
    sleep(120)
    user.save()


@shared_task
def check_user_is_active_for_register(phone) : 
    user = get_user_model().objects.get(phone=phone)
    send_sms(user.phone,user.otp_code)
    sleep(120)
    user = get_user_model().objects.get(phone=phone)
    if not user.is_active : 
        user.delete()
    else :
        user.save()