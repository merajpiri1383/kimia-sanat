from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.contrib.auth import get_user_model
import re
from authentication.tasks import check_user_is_active_for_register,send_otp
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from user.api.serializers import UserSerializer
from authentication.throttling import ResendOtpCodeThrottle


regex_phone = re.compile("^0[0-9]{10}$")


# ورود 
class LoginAPIView (APIView) : 

    @swagger_auto_schema(
        operation_summary="ورود یا ثبت نام",
        operation_description="""اگر شماره وجود نداشته باشه و کاربر بعد از 120 ثانیه کد تایید
        رو وارد نکنه کاربر حذف میشه 
        ارسال کد تایید""",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "phone" : openapi.Schema(type=openapi.TYPE_STRING,description="11 character and start with 0"),
            },
            required=["phone"]
        ),
        responses={
            200 : "ok"
        }
    )
    def post(self,request)  :
        phone = request.data.get("phone")
        if not phone : 
            return Response({'detail' : "phone is required ."},status.HTTP_400_BAD_REQUEST)
        if not regex_phone.findall(phone) :
            Response({'detail' : 'invalid phone number'},status.HTTP_400_BAD_REQUEST)
        user,created = get_user_model().objects.get_or_create(phone=phone)
        if created : 
            check_user_is_active_for_register.apply_async(args=[phone])
        else :
            send_otp.apply_async(args=[phone])
        return Response({'detail' : "otp code has been sent ."},status.HTTP_200_OK)
    


# تایید شماره
class VerifyAPIView (APIView) : 

    @swagger_auto_schema(
        operation_summary="تایید شماره",
        operation_description="وارد کردن کد تایید و گرفتن توکن ها و تایید شماره",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone' : openapi.Schema(type=openapi.TYPE_STRING,description="شماره"),
                'otp' : openapi.Schema(type=openapi.TYPE_STRING,description="کد تایید"),
            },
            required=["phone","otp"]
        ),
        responses={
            200 : "give tokens",
            400 : "invalid otp code",
            404 : "invalid number ",
        }
    )
    def post(self,request) : 
        phone = request.data.get("phone")
        otp = request.data.get("otp")
        if not phone :
            return Response({'detail' : 'phone field required .'},status.HTTP_400_BAD_REQUEST)
        if not otp : 
            return Response({'detail' : 'otp field required .'},status.HTTP_400_BAD_REQUEST)
        try : 
            user = get_user_model().objects.get(phone=phone)
        except :
            return Response({"detail" : "user not found ."},status.HTTP_400_BAD_REQUEST)
        if user.otp_code == otp : 
            user.is_active = True
            user.save()
            refresh_token = RefreshToken.for_user(user)
            data = {
                'user' : UserSerializer(user).data,
                'access' : str(refresh_token.access_token),
                'refresh' : str(refresh_token),
            }
            return Response(data,status.HTTP_200_OK)
        else :
            return Response({'detail' : 'invalid phone or otp code .'},status.HTTP_400_BAD_REQUEST)
        


# ارسال کد تایید 
class ResendOtpCodeAPIView (APIView) : 

    throttle_classes = [ResendOtpCodeThrottle]

    @swagger_auto_schema(
        operation_summary= "ارسال دوباره کد تایید",
        operation_description="""    
                شماره رو دریافت میکنه درصورتی که شماره از قبل وارد شده باشه کد تایید رو ارسال میکنه
                در غیر این صورت ارور ۴۰۴ 
        """,
        request_body= openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "phone" : openapi.Schema(type=openapi.TYPE_STRING,description="حتما با صفر شروع بشه و ۱۱ رقم باشه")
            }
        ),
        responses={
            200 : "otp code has been sent .",
            400 : "phone required / invalid phone ",
            404 : "user does not exist ."
        }
    )
    def post(self,request) : 
        phone = request.data.get("phone")
        if not phone : 
            return Response({'detail' : "phone is required ."},status.HTTP_400_BAD_REQUEST)
        if not regex_phone.findall(phone) :
            Response({'detail' : 'invalid phone number'},status.HTTP_400_BAD_REQUEST)
        try : 
            user = get_user_model().objects.get(phone=phone)
            send_otp.apply_async(args=[phone])
            return Response({'detail':'otp code has been sent .'},status.HTTP_200_OK)
        except : 
            return Response({'detail': 'phone not found .'},status.HTTP_404_NOT_FOUND)