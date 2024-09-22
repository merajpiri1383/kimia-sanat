from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from config.api.serializers import ContactUsSerializer,AboutUsSerializer,ConstactConsultSerializer
from config.models import ContactUs,AboutUs
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

 
# صفحه درباره ما 
class AbouteusAPIView(APIView) : 
    
    @swagger_auto_schema(
        operation_summary="about page", 
        operation_description="get info of aboute page"
    )
    def get(self,request) : 
        serializer = AboutUsSerializer(AboutUs.objects.first(),context={'request' : request})
        return Response(serializer.data,status.HTTP_200_OK)


# صفحه ارتباط با ما 
class ContactUsAPIView(APIView) : 

    @swagger_auto_schema(
        operation_summary="contact page",
        operation_description="get info of contact page"
    )
    def get(self,request) : 
        serializer = ContactUsSerializer(ContactUs.objects.first(),context={'request' : request}).data
        return Response(serializer,status.HTTP_200_OK) 
    


# ارسال فرم درخواست مشاوره 
class SendConsultAPIView (APIView) : 

    @swagger_auto_schema(
        operation_summary="ارسال درخواست مشاوره ",
        operation_description="ارسال درخواست مشاوره در صفحه ارتباط با ما",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name" : openapi.Schema(type=openapi.TYPE_STRING,description="نام"),
                "department" : openapi.Schema(type=openapi.TYPE_STRING,description="دپارتمان"),
                "phone" : openapi.Schema(type=openapi.TYPE_NUMBER,description="شماره"),
                "email" : openapi.Schema(type=openapi.TYPE_STRING,description="ایمیل"),
                "text" : openapi.Schema(type=openapi.TYPE_STRING,description="توضیحات"),
            },
            required=["name","department","phone","email","text"]
        ),
        responses={
            201 : "created",
            400 : 'bad requedt'
        }
    )
    def post(self,request) : 
        serializer = ConstactConsultSerializer(data=request.data)
        if serializer.is_valid() : 
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        else :
            return Response(serializer.errors,status.HTTP_200_OK)
        return Response({})