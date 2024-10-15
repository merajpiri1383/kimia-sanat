from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from user.api.serializers import LegaProfileSerializer,RealProfileSerializer,SocialMediaSerializer
from rest_framework.permissions import IsAuthenticated
from user.models import SocialMedia
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema 
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from product.api.serializers import ProductSimpleSerializer
from project.api.serializers import ProjectSimpleSerializer
from blog.api.serializers import BlogSimpleSerializer



# پروفایل حقیقی
class RealProfileAPIView (APIView) : 

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="پروفایل حقیقی",
        operation_description="درصورتی که کاربر اطلاعات حقیقی رو ارسال نکرده باشه ارور میده",
        responses={
            200 : RealProfileSerializer(),
            404 : "کاربر هنوز پروفایل حقیقی رو کامل نکرده"
        }
    )
    def get(self,request) : 
        try : 
            serializer = RealProfileSerializer(request.user.real_profile)
            return Response(serializer.data,status.HTTP_200_OK)
        except : 
            return Response({'detail': "user hasnt got real profile ."},status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        operation_summary="ارسال اطلاعات پروفایل حقیقی",
        operation_description="""
            درصورتی که کاربر پروفایل حقیقی داشته باشه ارور میده
            social_media :‌ باید اول لیست شبکه های اجتماعی رو از ادرس
            /user/social-media/ 
             آیدی اون شبکه اجتماعی رو بذاریselect بگیری بعد توی تگ
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name" : openapi.Schema(type=openapi.TYPE_STRING,description="نام"),
                "social_phone" : openapi.Schema(type=openapi.TYPE_STRING,description="شماره تلفن دارای شبکه اجتماعی"),
                "social_media" : openapi.Schema(type=openapi.TYPE_STRING,description="نوع شبکه اجتماعی شماره"),
                "national_id" : openapi.Schema(type=openapi.TYPE_STRING,description="کد ملی"),
                "email" : openapi.Schema(type=openapi.TYPE_STRING,description="ایمیل"),
                "address" : openapi.Schema(type=openapi.TYPE_STRING,description="آدرس"),
                "postal_code" : openapi.Schema(type=openapi.TYPE_STRING,description="کد پستی"),
            },
            required=["name","social_phone","national_id","email","address","postal_code"]
        )
    )
    def post(self,request) :
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = RealProfileSerializer(data=data)
        if serializer.is_valid () :
            serializer.save()
            request.user.is_real = True
            request.user.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="تغییر پروفایل حقیقی",
        operation_description="درصورتی که کاربر اطلاعات حقیقی رو ارسال نکرده باشه ارور میده",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name" : openapi.Schema(type=openapi.TYPE_STRING,description="نام"),
                "social_phone" : openapi.Schema(type=openapi.TYPE_NUMBER,description="شماره تلفن دارای شبکه اجتماعی"),
                "social_media" : openapi.Schema(type=openapi.TYPE_STRING,description="نوع شبکه اجتماعی شماره"),
                "national_id" : openapi.Schema(type=openapi.TYPE_STRING,description="کد ملی"),
                "email" : openapi.Schema(type=openapi.TYPE_STRING,description="ایمیل"),
                "address" : openapi.Schema(type=openapi.TYPE_STRING,description="آدرس"),
                "postal_code" : openapi.Schema(type=openapi.TYPE_NUMBER,description="کد پستی"),
            }
        ),
        responses={
            200 : RealProfileSerializer(),
            400 : "bad data"
        }
    )
    def put(self,request) : 
        try : 
            instance = request.user.real_profile
        except : 
            return Response({'detail' : 'user hasnt got real profile .'},status.HTTP_404_NOT_FOUND)
        serializer = RealProfileSerializer(data=request.data,instance=instance)
        if serializer.is_valid () : 
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        else :
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        

# پروفایل حقوقی
class LegalProfileAPIView (APIView) : 

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="دریافت اطلاعات پروفایل حقوقی",
        operation_description="درصورتی که کاربر پروفایل حقوقی رو ارسال نکرده باشه ارور میده",
        responses={
            200 : LegaProfileSerializer(),
            404 : "کاربر اطلاعات حقیقی رو ارسال نکرده"
        }
    )
    def get(self,request) : 
        try : 
            profile = request.user.legal_profile 
            serializer = LegaProfileSerializer(profile)
            return Response(serializer.data,status.HTTP_200_OK)
        except : 
            return Response({'detail' : 'user hasnt got legal profile .'},status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(
        operation_summary="ارسال اطلاعات پروفایل حقوقی",
        operation_description="""
            درصورتی که کاربر پروفایل حقوقی داشته باشه ارور میده
            social_media :‌ باید اول لیست شبکه های اجتماعی رو از ادرس
            /user/social-media/ 
             آیدی اون شبکه اجتماعی رو بذاریselect بگیری بعد توی تگ
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name" : openapi.Schema(type=openapi.TYPE_STRING,description="نام"),
                "social_phone" : openapi.Schema(type=openapi.TYPE_NUMBER,description="شماره تلفن دارای شبکه اجتماعی"),
                "social_media" : openapi.Schema(type=openapi.TYPE_STRING,description="نوع شبکه اجتماعی شماره"),
                "national_id" : openapi.Schema(type=openapi.TYPE_STRING,description="کد ملی"),
                "email" : openapi.Schema(type=openapi.TYPE_STRING,description="ایمیل"),
                "address" : openapi.Schema(type=openapi.TYPE_STRING,description="آدرس"),
                "postal_code" : openapi.Schema(type=openapi.TYPE_NUMBER,description="کد پستی"),
                "economic_code" : openapi.Schema(type=openapi.TYPE_STRING,description="کد اقتصادی"),
            },
            required=["name","social_phone","national_id","email","address","postal_code","economic_code"]
        ),
        responses={
            201 : LegaProfileSerializer(),
            400 : "bad data"
        }
    )
    def post(self,request) : 
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = LegaProfileSerializer(data=data)
        if serializer.is_valid () : 
            serializer.save()
            request.user.is_legal = True
            request.user.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else : 
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
        operation_summary="تغییر پروفایل حقوقی",
        operation_description="درصورتی که کاربر اطلاعات حقوقی رو ارسال نکرده باشه ارور میده",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name" : openapi.Schema(type=openapi.TYPE_STRING,description="نام"),
                "social_phone" : openapi.Schema(type=openapi.TYPE_NUMBER,description="شماره تلفن دارای شبکه اجتماعی"),
                "social_media" : openapi.Schema(type=openapi.TYPE_STRING,description="نوع شبکه اجتماعی شماره"),
                "national_id" : openapi.Schema(type=openapi.TYPE_STRING,description="کد ملی"),
                "email" : openapi.Schema(type=openapi.TYPE_STRING,description="ایمیل"),
                "address" : openapi.Schema(type=openapi.TYPE_STRING,description="آدرس"),
                "postal_code" : openapi.Schema(type=openapi.TYPE_NUMBER,description="کد پستی"),
                "economic_code" : openapi.Schema(type=openapi.TYPE_STRING,description="کد اقتصادی"),
            },
        ),
        responses={
            200 : LegaProfileSerializer(),
            400 : "bad data"
        }
    )
    def put(self,request) : 
        try : 
            instance = request.user.legal_profile
        except : 
            return Response({'detail' : 'user hasnt got legal profile .'},status.HTTP_404_NOT_FOUND)
        serializer = LegaProfileSerializer(data=request.data,instance=instance)
        if serializer.is_valid () :
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        else :
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        

# شبکه های اجتماعی
class SocialMediaAPIView(APIView) : 

    @swagger_auto_schema(
        operation_summary="لیست شبکه های اجتماعی",
        operation_description="""
            لیست شبکه های اجتماعی برای زمانی که کاربر اطاعات پروفایل می خواد پر کنه 
        """,
        responses={
            200 : SocialMediaSerializer(many=True),
        }
    )
    def get(self,request) : 
        serializer = SocialMediaSerializer(SocialMedia.objects.all(),many=True)
        return Response(serializer.data,status.HTTP_200_OK)
    

# موارد ذخیره شده 

class SavedItems (APIView) : 

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="موارد ذخیره شده",
        operation_description="""
            ?type=product => saved products 
            ?type=blog => saved blogs 
            ?type=project => saved projects
            default => saved products
        """
    )
    def get(self,request) :
        type = request.GET.get("type","product")
        queryset = []
        if type == "product" : 
            queryset = request.user.saved_products.all()
        elif type == "project" : 
            queryset = request.user.saved_projects.all()
        elif type == "blog" : 
            queryset = request.user.saved_blogs.all()

        paginator = Paginator(queryset,10)
        try : 
            result = paginator.page(request.GET.get("page",1))
        except EmptyPage : 
            result = paginator.page(1)
        except PageNotAnInteger : 
            result = paginator.page(1)

        if type == "product" : 
            results = ProductSimpleSerializer(result,many=True,context={'request':request}).data
        elif type == "project" : 
            results = ProjectSimpleSerializer(result,many=True,context={'request':request}).data
        elif type == "blog" : 
            results = BlogSimpleSerializer(result,many=True,context={'request':request}).data
        print(result.count)
        data = {
            "results" : results,
            "count" : paginator.count,
            "page_nums" : paginator.num_pages,
            "next_page" : f"{request.build_absolute_uri().split("?")[0]}?page={result.next_page_number()}&type={type}"
            if result.has_next() else None,
            "previous_page" : f"{request.build_absolute_uri().split("?")[0]}?page={result.previous_page_number()}&type={type}"
            if result.has_previous() else None,
        }
        return Response(data,status.HTTP_200_OK) 