from django.urls import path
from profuser.api import views


urlpatterns = [

    path('driver/',views.DriverListCreateAPIView.as_view(),name="driver-list"),

    path('driver/<driver_id>/',views.DriverDetailAPIView.as_view(),name="driver-detail"),

]