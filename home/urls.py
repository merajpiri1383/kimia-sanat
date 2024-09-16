from django.urls import path
from home.api import views

urlpatterns = [

    path('',views.HomePageAPIView.as_view(),name="home-page"),
]