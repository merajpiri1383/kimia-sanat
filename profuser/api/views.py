from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from utils.permissions import IsActiveOrNot
from profuser.api.serializers import DriverSerializer
from profuser.permissions import IsOwnDriverOrNot
from profuser.models import Driver



# لیست راننده ها
class DriverListCreateAPIView (APIView) : 

    permission_classes = [IsActiveOrNot]

    def get(self,request) : 
        serializer = DriverSerializer(request.user.drivers.all(),many=True)
        return Response(serializer.data,status.HTTP_200_OK)
    
    def post(self,request) : 
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid () : 
            driver = serializer.save()
            request.user.drivers.add(driver)
            return Response(serializer.data,status.HTTP_201_CREATED)
        else : 
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        


# جزیات راننده 
class DriverDetailAPIView (APIView) : 

    permission_classes = [IsOwnDriverOrNot]

    driver = None

    def dispatch(self, request,driver_id):
        try : 
            self.driver = Driver.objects.get(id=driver_id)
        except : pass 
        return super().dispatch(request,driver_id)
    
    def get(self,request,driver_id) :
        if not self.driver : return Response({'detail' : 'driver not found .'},status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request,self.driver)
        serializer = DriverSerializer(self.driver)
        return Response(serializer.data,status.HTTP_200_OK) 
    
    def put(self,request,driver_id) : 
        if not self.driver : return Response({'detail' : 'driver not found .'},status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request,self.driver)
        serializer = DriverSerializer(instance=self.driver,data=request.data)
        if serializer.is_valid() : 
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        else : 
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,driver_id): 
        if not self.driver : return Response({'detail' : 'driver not found .'},status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request,self.driver)
        self.driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)