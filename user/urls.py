from django.urls import path
from user.api import views

urlpatterns = [
    
    path('real-profile/',views.RealProfileAPIView.as_view(),name="real-profile"),

    path('legal-profile/',views.LegalProfileAPIView.as_view(),name="legal-profile"),
]