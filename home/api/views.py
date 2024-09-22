from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from template


# صفحه هوم 
class HomePageAPIView (APIView) : 

    def get(self,request) : 
        data = {
        }
        return Response(data,status.HTTP_200_OK)