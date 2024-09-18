from rest_framework import serializers
from config.models import (ContactItem,ContactTitle,ContactUs,SocialContact,SocialTitle,AboutUs,Achievements
                           ,Feq,FeqTitle,OrderGuideTitle,OrderingGuide,Story)
from project.api.serializers import ProjectSimpleSerializer


# مدل درباره ما 

class StorySerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Story
        exclude = ["id","about"]

class AchievementsSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Achievements
        exclude = ["id","about"]

class OrderGuideTitleSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = OrderGuideTitle
        exclude = ["id","about"]

class OrderingGuideSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = OrderingGuide
        exclude = ["id","about"]

class FeqTitleSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = FeqTitle
        exclude = ["id","about"]

class FeqSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Feq
        exclude = ["id","about"]


class AboutUsSerializer (serializers.ModelSerializer) : 
    projects = ProjectSimpleSerializer(many=True)
    class Meta : 
        model = AboutUs
        exclude = ["id"]
    
    def to_representation (self,instance,**kwargs) : 
        context = super().to_representation(instance,**kwargs)
        try : 
            context["story"] = StorySerializer(instance.story,context=self.context).data
        except :
            context["story"] = {}
        
        try :
            context["achievement_card"] =  AchievementsSerializer(instance.achievements,context=self.context).data
        except :
            context["achievement_card"] = {}
        try :
            context["order_guide_card"] = OrderGuideTitleSerializer(instance.order_guide_title,context=self.context).data
        except : 
            context["order_guide_card"] = {}
        context["order_guide_items"] = OrderingGuideSerializer(instance.ordering_items,many=True,context=self.context).data
        try : 
            context["feq_card"] = FeqTitleSerializer(instance.feq_title,context=self.context).data
        except :
            context["feq_card"] = {}
        context["feq_items"] = FeqSerializer(instance.feqs,many=True).data
        return context


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

class SocialContactSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = SocialContact
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
        context["socials"] = SocialContactSerializer(instance.contact_social.all(),many=True,context=self.context).data
        return context