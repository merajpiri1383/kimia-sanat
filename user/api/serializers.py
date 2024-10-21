from rest_framework import serializers
from django.contrib.auth import get_user_model
from user.models import RealProfile,LegalProfile,SocialMedia
import re
from rest_framework.exceptions import ValidationError

phone_regex = re.compile("^0[0-9]{10}$") 
telephone_regex = re.compile("^[0-9]{6,}$")


# مدل شبکه اجتماعی
class SocialMediaSerializer (serializers.ModelSerializer) : 
    
    class Meta : 
        model = SocialMedia
        fields = "__all__"


# مدل کاربر
class UserSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = get_user_model()
        exclude = ["is_superuser","otp_code","last_login","password","is_staff","user_permissions"]


# مدل پروفایل حقیقی 
class RealProfileSerializer (serializers.ModelSerializer) : 

    social_media = SocialMediaSerializer(many=True,required=False)

    class Meta : 
        model = RealProfile
        fields = "__all__"

    def __init__(self,instance=None,**kwargs) : 
        if instance : 
            kwargs["partial"] = True
        return super().__init__(instance,**kwargs)
    
    def validate(self,attrs) : 
        if not self.instance and not telephone_regex.findall(attrs["telephone"]) : 
            raise ValidationError({'telephone' : 'invalid phone number , must be more than 5 character .'})
        if self.instance and "telephone" in attrs and not telephone_regex.findall(attrs["telephone"]) : 
            raise ValidationError({'telephoe' : 'invalid phone number , must be more than 5 character .'})
        return super().validate(attrs)
    
    def to_representation(self, instance):
        context = super().to_representation(instance)
        if "request" in self.context : 
            context["phone"] = self.context["request"].user.phone
        return context
    

# مدل پروفایل حقوقی
class LegaProfileSerializer (serializers.ModelSerializer) : 

    social_media = SocialMediaSerializer(many=True,required=False)

    class Meta : 
        model = LegalProfile
        fields = "__all__"
    
    def __init__(self,instance=None,**kwargs) : 
        if instance : 
            kwargs["partial"] = True
        return super().__init__(instance,**kwargs)
    

    def validate(self,attrs) : 
        if not self.instance and not telephone_regex.findall(attrs["telephone"]) : 
            raise ValidationError({'telephone' : 'invalid phone number , must be more than 5 character .'})
        if self.instance and "telephone" in attrs and not telephone_regex.findall(attrs["telephone"]) : 
            raise ValidationError({'telephoe' : 'invalid phone number , must be more than 5 character .'})
        return super().validate(attrs)
    
class ImageSerializer (serializers.Serializer) : 
    profile_image = serializers.ImageField(read_only=True)

# دیتا کاربر برای navbar 

class UserInfoSerializer (serializers.ModelSerializer) : 

    name = serializers.SerializerMethodField("get_name")

    def get_name (self,obj) : 
        if hasattr(obj,"real_profile") : 
            return obj.real_profile.name
        elif hasattr(obj,'legal_profile') : 
            return obj.legal_profile.name
        return None

    class Meta : 
        model = get_user_model()
        fields = ["id","phone","name","is_active","is_legal","is_real","is_panel_active"]

    def to_representation(self,instance,**kwargs) : 
        context = super().to_representation(instance,**kwargs)
        if hasattr(instance,"real_profile") : 
            context["url"] = ImageSerializer(
                instance.real_profile,
                context=self.context).data
        elif hasattr(instance,'legal_profile') : 
            context["url"] = ImageSerializer(
                instance.legal_profile,
                context=self.context
            ).data
        else :
            context["url"] = None
        return context