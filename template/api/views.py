from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.generics import ListAPIView
from rest_framework.response import Response 
from template.api.serializers import (HeaderSerializer,FooterSerializer,CommingSoonSerializer,BlogTtileSerializer,
        ProjectTitleSerializer,AchievementCardSerializer,AnswerQuestionTitleSerializer,ProductTitleSerializer,
        FirstPageSerilizer,ConsultSerializer,LicenseSerializer,SliderSerializer)
from template.models import (Header,Footer,CommingSoon,BlogTitle,ProjectTitle,AchievementCard,
        AnswerQuestionTitle,ProductTitle,FirstPageContent,License,Slider)
from drf_yasg.utils import swagger_auto_schema
from template.pagination import LicensePagination



# هدر و فوتر 
class TemplateAPIView (APIView) : 

    def get(self,request) :  
        data = {
            'header' : HeaderSerializer(Header.objects.first(),context={"request":request}).data,
            'footer' : FooterSerializer(Footer.objects.first(),context={'request' : request}).data
        }
        comming_soon = CommingSoon.objects.first()
        if  comming_soon : 
            data["comming_soon"] = CommingSoonSerializer(comming_soon,context={'request':request}).data
        return Response(data,status.HTTP_200_OK)
    


# صفحه اصلی
class HomePageAPIView (APIView) : 
 
    def get(self,request) : 
        data = {
            'sliders' : SliderSerializer(Slider.objects.all(),many=True,context={'request' : request}).data,
            'first_page' : FirstPageSerilizer(FirstPageContent.objects.first(),context={'request':request}).data,
            'product_card' : ProductTitleSerializer(ProductTitle.objects.first(),context={'request':request}).data,
            'answer_question_card' : AnswerQuestionTitleSerializer(
                AnswerQuestionTitle.objects.first(),
                context={'request' : request}
                ).data,
            'achievement_card' : AchievementCardSerializer(
                AchievementCard.objects.first()
                ,context={'request':request}
                ).data,
            'project_card' : ProjectTitleSerializer(ProjectTitle.objects.first(),context={'request':request}).data, 
            'blog_card' : BlogTtileSerializer(BlogTitle.objects.first(),context={"request":request}).data
        }
        return Response(data,status.HTTP_200_OK)
    


# ارسال فرم مشاوره
class SendConsultAPIView(APIView) : 

    @swagger_auto_schema(
        operation_summary="ارسال درخواست مشاوره",
        operation_description="ارسال درخواست مشاوره در صفحه هوم"
    )
    def post(self,request) : 
        serializer = ConsultSerializer(data=request.data)
        if serializer.is_valid() : 
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        else :
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        


# لیست گواهی نامه ها 
class LicenseListAPIView (ListAPIView) : 
    serializer_class = LicenseSerializer
    queryset = License.objects.all()
    pagination_class = LicensePagination