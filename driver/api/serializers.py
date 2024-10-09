from rest_framework import serializers 
from driver.models import Driver
from rest_framework.validators import ValidationError
import re

phone_regex = re.compile("0[0-9]{10}")




# مدل راننده 
class DriverSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = Driver
        fields = "__all__"
    
    def __init__(self,instance=None,**kwargs) :
        if instance : 
            kwargs["partial"] = True
        return super().__init__(instance,**kwargs) 

    def validate(self,attrs) : 
        if "phone" in attrs and not phone_regex.findall(attrs["phone"]) : 
            raise ValidationError({'phone' : "please enter correct phone number ."})
        return super().validate(attrs)