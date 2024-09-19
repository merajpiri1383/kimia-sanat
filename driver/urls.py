from django.urls import path
from driver.api import views


urlpatterns = [

    path('',views.DriverListCreateAPIView.as_view(),name="driver-list"),

    path('<driver_id>/',views.DriverDetailAPIView.as_view(),name="driver-detail"),

]