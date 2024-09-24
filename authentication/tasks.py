from celery import shared_task
from django.contrib.auth import get_user_model
from time import sleep


@shared_task
def send_otp (phone) : 
    user = get_user_model().objects.get(phone=phone)
    print(user.otp_code)
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