from django.urls import path
from notification.api import views

urlpatterns = [

    path("page/",views.NotificationPageAPIView.as_view(),name="notification-page"),

    path('<notification_id>/read/',views.ReadNotificationAPIView.as_view(),name="read-notification"),
]