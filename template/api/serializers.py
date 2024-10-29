from rest_framework import serializers
from template.models import CommingSoon,LoginPage,LoginPageSlide
from template.footer.serializers import * 
from template.header.serializers import * 
from template.panel.serializers import * 
from template.main.serializers import *

    
# comming soon

class CommingSoonSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = CommingSoon
        exclude = ["id"]


# login page 

class LoginPageSlideSerializer (serializers.ModelSerializer) : 

    class Meta :
        model = LoginPageSlide
        exclude = ["id","page"]

class LoginPageSerializer (serializers.ModelSerializer) : 

    sliders = LoginPageSlideSerializer(many=True)

    
    class Meta : 
        model = LoginPage
        exclude = ["id"]
