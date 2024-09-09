from django.urls import path
from config.api import views

urlpatterns = [
    
    path('about/',views.AbouteusAPIView.as_view(),name="about"),
    
]