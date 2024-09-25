from django.urls import path
from authentication.api import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    path('login/',views.LoginAPIView.as_view(),name='login'),

    path('verify/',views.VerifyAPIView.as_view(),name="verify"),

    path('resend-otp/',views.ResendOtpCodeAPIView.as_view(),name="resend-otp"),

    path('refresh/token/',TokenRefreshView.as_view(),name="refresh"),
]