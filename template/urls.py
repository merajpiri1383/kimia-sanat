from django.urls import path
from template.api import views

urlpatterns = [
    
    path('',views.TemplateAPIView.as_view(),name="template"),

    path('home/',views.HomePageAPIView.as_view(),name="home-page"),

    path('send-consult/',views.SendConsultAPIView.as_view(),name="send-consult"),

    path('home/achievements/',views.AcheivementTitleAPIView.as_view(),name="achievement-list"),
] 