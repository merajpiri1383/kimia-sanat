from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.response import Response 
from template.api.serializers import (HeaderSerializer,FooterSerializer,CommingSoonSerializer,BlogTtileSerializer,
        ProjectTitleSerializer,AchievementCardSerializer,AnswerQuestionTitleSerializer,ProductTitleSerializer,
        SliderSerializer,FirstPageSerilizer)
from template.models import (Header,Footer,CommingSoon,BlogTitle,ProjectTitle,AchievementCard,
        AnswerQuestionTitle,ProductTitle,Slider,FirstPageContent)

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
            'slider' : SliderSerializer(Slider.objects.first(),context={'request' : request}).data,
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