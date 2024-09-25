from rest_framework import serializers
from django.contrib.auth import get_user_model
from user.models import RealProfile,LegalProfile


# مدل کاربر
class UserSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = get_user_model()
        exclude = ["is_superuser","otp_code","last_login","password","is_staff","user_permissions"]


# مدل پروفایل حقیقی 
class RealProfileSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = RealProfile
        fields = "__all__"
    

# مدل پروفایل حقوقی
class LegaProfileSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = LegalProfile
        fields = "__all__"