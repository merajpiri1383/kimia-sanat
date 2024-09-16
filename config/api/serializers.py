from rest_framework import serializers
from config.models import Settings,Achievements,Feq,OrderingGuide,Story,SocialContact,ContactItem

# دستاورد ها ما
class AchievementSerializer(serializers.ModelSerializer) : 
    
    class Meta :
        model = Achievements
        exclude = ["id","settings"]


# سوالات متداول
class FeqSerializer(serializers.ModelSerializer) : 
    
    class Meta :
        model = Feq
        exclude = ["id","settings"]


# راهنمای سفارش
class OrderingGuideSerializer(serializers.ModelSerializer) : 
    
    class Meta :
        model = OrderingGuide
        exclude = ["id","settings"]


# داستان ما
class StorySerializer(serializers.ModelSerializer) : 
    
    class Meta :
        model = Story
        exclude = ["id","settings"]

# شبکه های اجتماعی
class SocialContactSerializer(serializers.ModelSerializer) : 

    class Meta : 
        model = SocialContact
        exclude = ["id","settings"]


# راه های ارتباطی
class ContactItemSerializer(serializers.ModelSerializer) : 

    class Meta : 
        model = ContactItem
        exclude = ["id","settings"]


# تنظیمات ساده برای صفحه هوم
class SimpleSettingSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = Settings
        fields = ["logo"]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        try :
            context["acheivments"] = AchievementSerializer(instance.achievements).data
        except : 
            context["acheivments"] = []
        context["contacts"] = ContactItemSerializer(instance.contact_items.all(),many=True).data
        return context