from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from user.api.serializers import LegaProfileSerializer,RealProfileSerializer
from rest_framework.permissions import IsAuthenticated


# پروفایل حقیقی
class RealProfileAPIView (APIView) : 

    permission_classes = [IsAuthenticated]


    def post(self,request) :
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = RealProfileSerializer(data=data)
        if serializer.is_valid () :
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        else :
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        

# پروفایل حقوقی
class LegalProfileAPIView (APIView) : 

    permission_classes = [IsAuthenticated]

    def post(self,request) : 
        serializer = LegaProfileSerializer(data=request.data)
        if serializer.is_valid () : 
            return Response(serializer.data,status.HTTP_200_OK)
        else : 
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)