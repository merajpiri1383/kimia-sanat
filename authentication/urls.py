from django.urls import path
from authentication.api import views


urlpatterns = [

    path('refresh/token/',views.CustomTokenRefreshView.as_view(),name="refresh"),

    path('login/',views.LoginAPIView.as_view(),name='login'),

    path('verify/',views.VerifyAPIView.as_view(),name="verify"),

    path('resend-otp/',views.ResendOtpCodeAPIView.as_view(),name="resend-otp"),
]