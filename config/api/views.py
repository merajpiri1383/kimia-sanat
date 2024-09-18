from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from config.api.serializers import ContactUsSerializer,AboutUsSerializer
from config.models import ContactUs,AboutUs

 
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