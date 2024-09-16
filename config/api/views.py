from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from config.models import Settings
from config.api.serializers import (AchievementSerializer,StorySerializer,FeqSerializer,OrderingGuideSerializer,
                                    SocialContactSerializer,ContactItemSerializer)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from project.models import Project
from project.api.serializers import ProjectSimpleSerializer

 
# صفحه درباره ما 
class AbouteusAPIView(APIView) : 
    
    @swagger_auto_schema(
        operation_summary="about page",
        operation_description="get info of aboute page"
    )
    def get(self,request) : 
        setting = Settings.objects.get(id=1)
        data = {}
        try : data["story"] = StorySerializer(setting.story).data
        except : data["story"] = {}
        try : data["achievements"] = AchievementSerializer(setting.achievements).data
        except : data["achievements"] = {}
        data["feqs"] = FeqSerializer(setting.feqs.all(),many=True).data
        data["order_guides"] = OrderingGuideSerializer(setting.ordering_guide.all(),many=True).data
        data["projects"] = ProjectSimpleSerializer(Project.objects.filter(is_completed=True)[:3],many=True,context={'request':request}).data
        return Response(data,status.HTTP_200_OK)


# صفحه ارتباط با ما
class ContactUsAPIView(APIView) : 

    @swagger_auto_schema(
        operation_summary="contact page",
        operation_description="get info of contact page"
    )
    def get(self,request) : 
        setting = Settings.objects.get(id=1)
        return Response({
            "socials" : SocialContactSerializer(setting.socials.all(),many=True,context={"request":request}).data,
            "contacts" : ContactItemSerializer(setting.contact_items.all(),many=True).data
        },status.HTTP_200_OK)