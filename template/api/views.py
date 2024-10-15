from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.response import Response 
from template.api.serializers import (HeaderSerializer,FooterSerializer,CommingSoonSerializer,BlogTtileSerializer,
        ProjectTitleSerializer,AchievementCardSerializer,AnswerQuestionTitleSerializer,ProductTitleSerializer,
        FirstPageSerilizer,ConsultSerializer,SliderSerializer,AchievementTitleSerializer,AchievementSerializer,
        CardNumbersPageSerializer)
from template.models import (Header,Footer,CommingSoon,BlogTitle,ProjectTitle,AchievementCard,
        AnswerQuestionTitle,ProductTitle,FirstPageContent,Slider,AchievementTitle,Achievement,
        CompanyCardsPage)
from drf_yasg.utils import swagger_auto_schema
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from drf_yasg import openapi
from project.models import Project
from product.models import Product
from blog.models import Blog
from blog.api.serializers import BlogSimpleSerializer
from product.api.serializers import ProductSimpleSerializer
from project.api.serializers import ProjectSimpleSerializer
from django.contrib.postgres.search import SearchQuery,SearchVector,SearchRank



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
        operation_description="ارسال درخواست مشاوره در صفحه هوم",
        request_body = openapi.Schema(
            type = openapi.TYPE_OBJECT,
            properties = {
                "name" : openapi.Schema(type=openapi.TYPE_STRING,description="نام حداکثر ۲۵۶ کاراکتر"),
                "person" : openapi.Schema(type=openapi.TYPE_STRING,description="نوع شخص یا real یا legal"),
                "phone" : openapi.Schema(type=openapi.TYPE_STRING,description="شماره تلفن ۱۱ رقم و با صفر شروع میشه"),
                "email" : openapi.Schema(type=openapi.TYPE_STRING,description="ایمیل"),
                "text" : openapi.Schema(type=openapi.TYPE_STRING,description="توضیحات "),
            },
            required=["name","person","phone","email","text"]
        ),
        responses={
            201 : ConsultSerializer(),
            400 : "bad data "
        }
    )
    def post(self,request) : 
        serializer = ConsultSerializer(data=request.data)
        if serializer.is_valid() : 
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        else :
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        


# دستاورد ها

class AcheivementTitleAPIView (APIView) : 

    @swagger_auto_schema(
        operation_summary="پاپ آپ دستاورد ها"
    )
    def get(self,request) :

        object = AchievementTitle.objects.first()

        paginator = Paginator(Achievement.objects.all().order_by("id"),per_page=10)

        try :
            items = paginator.page(request.GET.get("page",1))
        except PageNotAnInteger : 
            items = paginator.page(1)
        except EmptyPage : 
            items = paginator.page(1)

        data = {
            "titles" : AchievementTitleSerializer(object).data,
            "items" : AchievementSerializer(items,context={'request' : request},many=True).data,
            "count" : paginator.count,
            "pages" : paginator.num_pages,
        }
        if items.has_next() : 
            data["next_page"] = f"{request.build_absolute_uri().split("?")[0]}?page={items.next_page_number()}"
        else :
            data["next_page"] = None
        if items.has_previous() :
            data["previous_page"] = f"{request.build_absolute_uri().split("?")[0]}?page={items.previous_page_number()}"
        else :
            data["previous_page"] = None
        return Response(data,status.HTTP_200_OK)
    



# سرچ 
class SearchAPIView (APIView) : 

    @swagger_auto_schema(
        operation_summary="جست و جو",
        operation_description="""
            کلمه جست و جو باید با پارامتر query  بیاد
            type=blog => جست و جوی مقاله
            type=project => جست و جو پروژه
            type=product => جست و جوی محصول
            اگر پارامتر type رو نفرستی همه رو جست و جو میکنه
        """
    )
    def get(self,request) : 
        data = {}

        query = request.GET.get("query")

        type = request.GET.get("type")

        if query :
            query = SearchQuery(query)
            if not type or type == "blog" : 
                blogs =  Blog.objects.filter(is_published=True).annotate(rank=SearchRank(
                        vector = SearchVector("title","description"),
                        query = query
                        )).filter(rank__gt=0.001).order_by("-rank")
                data["blogs"] = BlogSimpleSerializer(blogs,context={'request':request},many=True).data
            
            if not type or type == "product" : 
                products = Product.objects.annotate(rank=SearchRank(
                    vector = SearchVector("title","description"),
                    query = query
                )).filter(rank__gt=0.001).order_by("-rank")
                data["products"] = ProductSimpleSerializer(products,many=True,context={'request':request}).data
            
            if not type or type == "project" : 
                projects = Project.objects.annotate(rank=SearchRank(
                    vector = SearchVector("name","description"),
                    query = query
                )).filter(rank__gt=0.001).order_by("-rank")
                data["projects"] = ProjectSimpleSerializer(projects,context={'request':request},many=True).data
        else :
            data = {
                "projects" : [] , 
                "products" : [] , 
                "blogs" : []
            }
        return Response(data,status.HTTP_200_OK)
    

# صفحه شماره کارت های شرکت

class CardNumberPageAPIView (APIView) : 

    @swagger_auto_schema(
        operation_summary="صفحه شماره کارت های شرکت",
        responses={
            200 : CardNumbersPageSerializer()
        }
    )
    def get(self,request) : 
        page = CompanyCardsPage.objects.first()
        serializer = CardNumbersPageSerializer(page,context={'request':request})
        return Response(serializer.data,status.HTTP_200_OK)