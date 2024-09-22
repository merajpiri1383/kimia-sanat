from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from utils.permissions import IsActiveOrNot
from driver.api.serializers import DriverSerializer
from driver.permissions import IsOwnDriverOrNot
from driver.models import Driver
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage



# لیست راننده ها
class DriverListCreateAPIView (APIView) : 

    permission_classes = [IsActiveOrNot]

    @swagger_auto_schema(
        operation_description="لیست راننده های کاربر ",
        operation_summary="لیست راننده ها"
    )
    def get(self,request) : 
        paginator = Paginator(request.user.drivers.all().order_by("-created"),per_page=10)
        try :
            drivers = paginator.page(request.GET.get("page",1))
        except EmptyPage : 
            drivers = paginator.page(1) 
        except PageNotAnInteger : 
            drivers = paginator.page(1)
        data = {
            'drivers' : DriverSerializer(drivers,many=True).data,
        }
        if drivers.has_next() : 
            data["next_page"] = f"{request.build_absolute_uri().split("?")[0]}?page={drivers.next_page_number()}"
        if drivers.has_previous() : 
            data["previous_page"] = f"{request.build_absolute_uri().split("?")[0]}?page={drivers.previous_page_number()}"
        return Response(data,status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary="افزودن راننده",
        operation_description="افزودن راننده جدید توسط کاربر",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name' : openapi.Schema(type=openapi.TYPE_STRING,description="نام راننده"), 
                'license_plate' : openapi.Schema(type=openapi.TYPE_STRING,description="پلاک ماشین"), 
                'car' : openapi.Schema(type=openapi.TYPE_STRING,description="نام ماشین"), 
                'phone' : openapi.Schema(type=openapi.TYPE_STRING,description="شماره راننده"), 
                'national_id' : openapi.Schema(type=openapi.TYPE_STRING,description="کد ملی راننده"), 
            },
            required=["name","license_plate","car","phone","national_id"]
        )
    )
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
    
    @swagger_auto_schema(
        operation_summary="جزيیات راننده",
        operation_description="جزيیات راننده ",
        responses={
            200 : DriverSerializer(),
            404 : "راننده ای با این id پیدا نشد"
        }
    )
    def get(self,request,driver_id) :
        if not self.driver : return Response({'detail' : 'driver not found .'},status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request,self.driver)
        serializer = DriverSerializer(self.driver)
        return Response(serializer.data,status.HTTP_200_OK) 
    
    @swagger_auto_schema(
        operation_summary="تغییر راننده",
        operation_description="تغییر راننده توسط کاربر",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name' : openapi.Schema(type=openapi.TYPE_STRING,description="نام راننده"), 
                'license_plate' : openapi.Schema(type=openapi.TYPE_STRING,description="پلاک ماشین"), 
                'car' : openapi.Schema(type=openapi.TYPE_STRING,description="نام ماشین"), 
                'phone' : openapi.Schema(type=openapi.TYPE_STRING,description="شماره راننده"), 
                'national_id' : openapi.Schema(type=openapi.TYPE_STRING,description="کد ملی راننده"), 
            }
        )
    )
    def put(self,request,driver_id) : 
        if not self.driver : return Response({'detail' : 'driver not found .'},status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request,self.driver)
        serializer = DriverSerializer(instance=self.driver,data=request.data)
        if serializer.is_valid() : 
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        else : 
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="حذف راننده ",
        operation_summary="حذف راننده",
        responses={
            204 : "با موفقیت حذف شد",
            404 : "راننده ای پیدا نشد"
        }
    )
    def delete(self,request,driver_id): 
        if not self.driver : return Response({'detail' : 'driver not found .'},status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request,self.driver)
        self.driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)