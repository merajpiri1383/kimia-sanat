from rest_framework import serializers
from config.models import (
    ContactItem,
    ContactTitle,
    ContactUs,
    SocialTitle,
    Location
)

# مدل تماس با ما 
class ContactItemSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = ContactItem
        exclude = ["id","contact"]

class ContactTitleSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = ContactTitle
        exclude = ["id","contact"]

class SocialTitleSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = SocialTitle
        exclude = ["id","contact"]

class LocationSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Location
        exclude = ["id","contact"]

class ContactUsSerializer (serializers.ModelSerializer) : 
    
    class Meta : 
        model = ContactUs
        exclude = ["id"]

    def to_representation(self,instance,**kwargs) : 
        context = super().to_representation(instance,**kwargs)
        try : 
            context["contact_us_card"] = ContactTitleSerializer(instance.contact_title,context=self.context).data
        except :
            context["contact_us_card"] = {}
        context["contact_us_card_items"] = ContactItemSerializer(instance.contact_items.all(),many=True).data
        try :
            context["social_card"] = SocialTitleSerializer(instance.social_title,context=self.context).data
        except : 
            context["social_card"] = {}

        try : 
            context["location"] = LocationSerializer(instance.location,context=self.context).data
        except : 
            context["location"] = {}
        return context 