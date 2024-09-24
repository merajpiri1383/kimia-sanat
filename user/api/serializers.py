from rest_framework import serializers
from django.contrib.auth import get_user_model


# مدل کاربر
class UserSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = get_user_model()
        exclude = ["is_superuser","otp_code","last_login","password","is_staff","user_permissions"]