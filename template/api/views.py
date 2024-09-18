from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.response import Response 
from template.api.serializers import HeaderSerializer,FooterSerializer
from template.models import Header,Footer

# هدر و فوتر 
class TemplateAPIView (APIView) : 

    def get(self,request) : 
        data = {
            'header' : HeaderSerializer(Header.objects.first(),context={"request":request}).data,
            'footer' : FooterSerializer(Footer.objects.first(),context={'request' : request}).data
        }
        return Response(data,status.HTTP_200_OK)