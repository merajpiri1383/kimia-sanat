from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from home.models import Slider,License
from home.api.serializers import SliderSerializer,LicenseSerializer
from product.models import Category
from product.api.serializers import CategorySerializer
from project.models import Project
from project.api.serializers import ProjectSimpleSerializer
from blog.models import Blog
from blog.api.serializers import BlogSimpleSerializer
from config.models import Achievements
from config.api.serializers import AchievementSerializer


# صفحه هوم 
class HomePageAPIView (APIView) : 

    def get(self,request) : 
        data = {
            'slider' : SliderSerializer(Slider.objects.first(),context={'request' : request}).data,
            'licenses' : LicenseSerializer(License.objects.all(),context={"request": request},many=True).data,
            'categories' : CategorySerializer(Category.objects.all()[:3],many=True,context={'request':request}).data,
            'achievments' : AchievementSerializer(Achievements.objects.all(),many=True).data,
            'projects' : ProjectSimpleSerializer(Project.objects.filter(is_completed=True)[:3],many=True,context={'request':request}).data,
            'blogs' : BlogSimpleSerializer(Blog.objects.filter(is_published=True).order_by("-created_date")[:4],many=True,context={'request':request}).data
        }
        return Response(data,status.HTTP_200_OK)