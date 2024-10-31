from rest_framework import serializers
from template.footer.models import (
    CategoryFooter,
    CustomerClub,
    ElectroLicense,
    Footer,
    FooterFeq,
    FooterLink,
    PhoneFooter
)
from rest_framework.exceptions import ValidationError
import re

phone_regex = re.compile("0[0-9]{10}")



# مدل فوتر 

class CategoryFooterSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = CategoryFooter
        exclude = ["id","footer"]

class FooterPhoneSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = PhoneFooter
        exclude = ["id","footer"]

class FooterLinkSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = FooterLink
        exclude = ["id","footer"]

class ElectroLicenseSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = ElectroLicense
        exclude = ["id","footer"]


class FooterFeqSerializer ( serializers.ModelSerializer ) : 
    class Meta : 
        model = FooterFeq
        exclude = ["id","footer"] 

class FooterSerializer (serializers.ModelSerializer) : 

    phones_fax = serializers.SerializerMethodField("get_phones_fax")

    phones_constant = serializers.SerializerMethodField("get_phones_constant")

    def get_phones_fax (self,obj) : 
        return FooterPhoneSerializer(obj.phones.filter(is_fax=True),many=True).data
    
    def get_phones_constant (self,obj) : 
        return FooterPhoneSerializer(obj.phones.filter(is_constant=True),many=True).data

    links = FooterLinkSerializer(many=True)

    categories = CategoryFooterSerializer(many=True)

    licenses = ElectroLicenseSerializer(many=True)

    feqs = FooterFeqSerializer(many=True)

    class Meta : 
        model = Footer
        exclude = ["id"]


# عضو باشگاه مشتریان

class CustomerClubSerializer (serializers.ModelSerializer) :

    def validate(self, attrs):
        if "phone" in attrs and not phone_regex.findall(attrs["phone"]) : 
            raise ValidationError({"phone": "invalid phone ."})
        return super().validate(attrs) 

    class Meta : 
        model = CustomerClub
        fields = "__all__"