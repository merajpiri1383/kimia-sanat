from rest_framework import serializers
from django.contrib.auth import get_user_model
from user.models import RealProfile,LegalProfile,SocialMedia
import re
from rest_framework.exceptions import ValidationError

phone_regex = re.compile("^0[0-9]{10}$") 
telephone_regex = re.compile("^[0-9]{6,}$")


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

    def __init__(self,instance=None,**kwargs) : 
        if instance : 
            kwargs["partial"] = True
        return super().__init__(instance,**kwargs)
    
    def validate(self,attrs) : 
        if not self.instance and not phone_regex.findall(attrs["social_phone"]) : 
            raise ValidationError({'social_phone' : 'invalid phone number .'})
        if not self.instance and not telephone_regex.findall(attrs["telephone"]) : 
            raise ValidationError({'telephone' : 'invalid phone number , must be more than 5 character .'})
        if self.instance and "social_phone" in attrs :
            raise ValidationError({'social_phone' : 'social_phone is not editable'})
        if self.instance and "telephone" in attrs and not telephone_regex.findall(attrs["telephone"]) : 
            raise ValidationError({'telephoe' : 'invalid phone number , must be more than 5 character .'})
        return super().validate(attrs)
    

# مدل پروفایل حقوقی
class LegaProfileSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = LegalProfile
        fields = "__all__"
    
    def __init__(self,instance=None,**kwargs) : 
        if instance : 
            kwargs["partial"] = True
        return super().__init__(instance,**kwargs)
    

    def validate(self,attrs) : 
        if not self.instance and not phone_regex.findall(attrs["social_phone"]) : 
            raise ValidationError({'social_phone' : 'invalid phone number .'})
        if not self.instance and not telephone_regex.findall(attrs["telephone"]) : 
            raise ValidationError({'telephone' : 'invalid phone number , must be more than 5 character .'})
        if self.instance and "social_phone" in attrs :
            raise ValidationError({'social_phone' : 'social_phone is not editable'})
        if self.instance and "telephone" in attrs and not telephone_regex.findall(attrs["telephone"]) : 
            raise ValidationError({'telephoe' : 'invalid phone number , must be more than 5 character .'})
        return super().validate(attrs)

# مدل شبکه اجتماعی
class SocialMediaSerializer (serializers.ModelSerializer) : 
    
    class Meta : 
        model = SocialMedia
        fields = "__all__"