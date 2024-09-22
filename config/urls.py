from django.urls import path
from config.api import views

urlpatterns = [
     
    path('about/',views.AbouteusAPIView.as_view(),name="about"),
    
    path('contact/',views.ContactUsAPIView.as_view(),name="contact"), 

    path('send-consult/',views.SendConsultAPIView.as_view(),name='send-consult')
] 