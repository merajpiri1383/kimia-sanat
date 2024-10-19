from django.urls import path
from driver.api import views


urlpatterns = [

    path('',views.DriverListCreateAPIView.as_view(),name="driver-list"),

    path('search/',views.SearchDriverAPIView.as_view(),name="serach-driver"),

    path('<driver_id>/',views.DriverDetailAPIView.as_view(),name="driver-detail"),

]