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
from product.models import Comment as ProductComment
from project.models import Comment as ProjectComment
from blog.models import Comment as BlogComment
from utils.permissions import IsActiveOrNot
from ticket.models import Ticket
from ticket.api.serializers import TicketSerializer
from driver.models import Driver
from order.models import Order
from order.api.serializers import OrderSimpleSerializer



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
            serializer = RealProfileSerializer(request.user.real_profile,context={'request':request})
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

            type : 
                1 => customer 
                2 => seller
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
                "type" : openapi.Schema(type=openapi.TYPE_STRING,description="نوع کاربر حقیقی"),
            },
            required=["name","social_phone","national_id","email","address","postal_code","type"]
        )
    )
    def post(self,request) :
        data = request.POST.copy()
        data["user"] = request.user.id
        serializer = RealProfileSerializer(data=data,context={'request':request})
        if serializer.is_valid () :
            serializer.save()
            request.user.is_real = True
            request.user.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="تغییر پروفایل حقیقی",
        operation_description="""درصورتی که کاربر اطلاعات حقیقی رو ارسال نکرده باشه ارور میده
            social_media :‌ باید اول لیست شبکه های اجتماعی رو از ادرس
            /user/social-media/ 
             آیدی اون شبکه اجتماعی رو بذاریselect بگیری بعد توی تگ""",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name" : openapi.Schema(type=openapi.TYPE_STRING,description="نام"),
                "social_media" : openapi.Schema(type=openapi.TYPE_STRING,description="نوع شبکه اجتماعی شماره"),
                "national_id" : openapi.Schema(type=openapi.TYPE_STRING,description="کد ملی"),
                "email" : openapi.Schema(type=openapi.TYPE_STRING,description="ایمیل"),
                "address" : openapi.Schema(type=openapi.TYPE_STRING,description="آدرس"),
                "postal_code" : openapi.Schema(type=openapi.TYPE_NUMBER,description="کد پستی"),
                "type" : openapi.Schema(type=openapi.TYPE_STRING,description="نوع کاربر حقیقی"),
                "profile_image" : openapi.Schema(type=openapi.TYPE_FILE,description="تصویر پروفایل")
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
        serializer = RealProfileSerializer(data=request.data,instance=instance,context={'request':request})
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
            serializer = LegaProfileSerializer(profile,context={'request':request})
            return Response(serializer.data,status.HTTP_200_OK)
        except : 
            return Response({'detail' : 'user hasnt got legal profile .'},status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(
        operation_summary="ارسال اطلاعات پروفایل حقوقی",
        operation_description="""
            درصورتی که کاربر پروفایل حقوقی داشته باشه ارور میده
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name" : openapi.Schema(type=openapi.TYPE_STRING,description="نام"),
                "national_id_company" : openapi.Schema(type=openapi.TYPE_STRING,description="کد ملی شرکت"),
                "email" : openapi.Schema(type=openapi.TYPE_STRING,description="ایمیل"),
                "address" : openapi.Schema(type=openapi.TYPE_STRING,description="آدرس"),
                "postal_code" : openapi.Schema(type=openapi.TYPE_NUMBER,description="کد پستی"),
                "economic_code" : openapi.Schema(type=openapi.TYPE_STRING,description="کد اقتصادی"),
                "telephone" : openapi.Schema(type=openapi.TYPE_STRING,description="تلفن"),
            },
            required=["name","national_id","email","address","postal_code","economic_code"]
        ),
        responses={
            201 : LegaProfileSerializer(),
            400 : "bad data"
        }
    )
    def post(self,request) : 
        data = request.POST.copy()
        data["user"] = request.user.id
        serializer = LegaProfileSerializer(data=data,context={'request':request})
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
                "social_media" : openapi.Schema(type=openapi.TYPE_STRING,description="نوع شبکه اجتماعی شماره"),
                "national_id" : openapi.Schema(type=openapi.TYPE_STRING,description="کد ملی"),
                "email" : openapi.Schema(type=openapi.TYPE_STRING,description="ایمیل"),
                "address" : openapi.Schema(type=openapi.TYPE_STRING,description="آدرس"),
                "postal_code" : openapi.Schema(type=openapi.TYPE_NUMBER,description="کد پستی"),
                "economic_code" : openapi.Schema(type=openapi.TYPE_STRING,description="کد اقتصادی"),
                "profile_image" : openapi.Schema(type=openapi.TYPE_FILE,description="تصویر پروفایل")
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
        serializer = LegaProfileSerializer(
            data=request.data,
            instance=instance,
            context={'request':request}
        )
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


# لایک و دیس لایک کامنت 

class CommentInteractionAPIView (APIView) : 

    permission_classes = [IsAuthenticated]

    comment = None

    def dispatch(self,request,comment_id) : 
        try : 
            self.comment = ProductComment.objects.get(id=comment_id)
        except : pass
        if not self.comment :
            try : 
                self.comment = ProjectComment.objects.get(id=comment_id)
            except : pass
        if not self.comment : 
            try : 
                self.comment = BlogComment.objects.get(id=comment_id)
            except : pass 
        return super().dispatch(request,comment_id)

    @swagger_auto_schema(
        operation_summary="لایک کامنت"
    )
    def post(self,request,comment_id) : 
        if not self.comment : return Response({'detail':'comment not found .'},status.HTTP_404_NOT_FOUND)
        self.comment.liked_by.add(request.user)
        self.comment.disliked_by.remove(request.user)
        return Response({"message": "comment liked successfully ."},status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary="دیس لایک کامنت"
    )
    def delete(self,request,comment_id) : 
        if not self.comment : return Response({'detail':'comment not found .'},status.HTTP_404_NOT_FOUND)
        self.comment.liked_by.remove(request.user)
        self.comment.disliked_by.add(request.user)
        return Response({"message": "comment disliked successfully ."},status.HTTP_200_OK)
    


# داشبورد

class DashboardAPIView (APIView) : 

    permission_classes = [IsActiveOrNot]
    @swagger_auto_schema(
        operation_summary="داشبورد پنل کاربر",
        operation_description="""
        ?type=ticket => تیکت های من
        ?type=last-order => سفارش های اخیر
        ?type=delivery-report => گزارش های تحویل بار
        """
    )
    def get(self,request) : 
        type = request.GET.get("type","ticket")
        if type == "ticket" : 
            objects = request.user.tickets.filter(reply_to=None).order_by("-created")
        elif type == "last-order" : 
            objects = request.user.orders.all().order_by("-created")
        elif type == "delivery-report" : 
            objects = request.user.orders.exclude(delivery_type=None).order_by("-created")
        paginator = Paginator(objects,8)
        try : 
            result = paginator.page(request.GET.get("type",1))
        except EmptyPage : 
            result = paginator.page(1)
        except PageNotAnInteger : 
            result = paginator.page(1)
        if type == "ticket" : 
            data = TicketSerializer(result,many=True).data
        else : 
            data = OrderSimpleSerializer(result,many=True,context={'request':request}).data
        data = {
            "counts" : {
                "orders" : request.user.orders.count(),
                "responsed_tickets" : request.user.tickets.filter(status="responsed").count(),
                "pending_tickets" : request.user.tickets.filter(status="pending-admin").count(),
                "drivers" : request.user.drivers.count()
            },
            "result" : data,
            "count" : paginator.count,
            "num_pages" : paginator.num_pages,
            "next_page" : f"{request.build_absolute_uri().split("?")[0]}?type={type}&page={result.next_page_number()}" 
            if result.has_next() else None,
            "previous_page" : f"{request.build_absolute_uri().split("?")[0]}?type={type}&page={result.previous_page_number()}" 
            if result.has_previous() else None,
        }
        print(paginator.num_pages)
        return Response(data,status.HTTP_200_OK)