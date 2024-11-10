from rest_framework import serializers
from config.models import (
    AboutUs,
    Achievements,
    Feq,
    FeqTitle,
    OrderGuideTitle,
    OrderingGuide,
    Story,
    StoryItem,
    ContactConsult
    )
from project.api.serializers import ProjectSimpleSerializer
import re
from rest_framework.exceptions import ValidationError

# مدل درباره ما 

class StoryItemSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = StoryItem
        exclude = ["id","story"]

class StorySerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Story
        exclude = ["id","about"]

    def to_representation(self,instance) : 
        context = super().to_representation(instance)
        context["items"] = StoryItemSerializer(instance.items.all(),many=True).data
        return context

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
        exclude = ["id","about","created"]

class FeqTitleSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = FeqTitle
        exclude = ["id","about"]

class FeqSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Feq
        exclude = ["id","about","created"]


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
    


# مدل فرم ارتباط با ما 

phone_regex = re.compile("^0[0-9]{10}$")
class ConstactConsultSerializer (serializers.ModelSerializer) :

    class Meta : 
        model = ContactConsult
        fields = "__all__"
    
    def validate(self,attrs) : 
        if not phone_regex.findall(attrs["phone"]) :
            raise ValidationError({'phone' : 'invalid phone number .'})
        return super().validate(attrs)