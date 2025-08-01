from django.urls import path
from template.api import views

urlpatterns = [
    
    path('',views.TemplateAPIView.as_view(),name="template"),

    path('home/',views.HomePageAPIView.as_view(),name="home-page"),

    path('send-consult/',views.SendConsultAPIView.as_view(),name="send-consult"),

    path('home/achievements/',views.AcheivementTitleAPIView.as_view(),name="achievement-list"),

    path('search/',views.SearchAPIView.as_view(),name="search"), 

    path("card-number-page/",views.CardNumberPageAPIView.as_view(),name="card-number-page"),

    path("add-customer-club/",views.AddCustomerClubAPIView.as_view(),name="customer-club"),
] 