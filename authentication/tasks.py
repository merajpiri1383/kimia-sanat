from celery import shared_task
from django.contrib.auth import get_user_model
from time import sleep
from authentication.sms import send_sms



@shared_task
def send_otp (phone) : 
    user = get_user_model().objects.get(phone=phone)
    try : 
        send_sms(phone,user.otp_code)
    except : pass 
    sleep(120)
    user.save()


@shared_task
def check_user_is_active_for_register(phone) : 
    user = get_user_model().objects.get(phone=phone)
    print(user.otp_code)
    sleep(120)
    user = get_user_model().objects.get(phone=phone)
    if not user.is_active : 
        user.delete()
    else :
        user.save()