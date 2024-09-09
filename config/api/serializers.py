from rest_framework import serializers
from config.models import Settings,Achievements,Feq,OrderingGuide,Story

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