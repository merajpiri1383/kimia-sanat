from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from notification.models import Notification,NotificationPage
from notification.api.serializers import NotificationPageSerializer,NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# صفحه اعلانات در پنل کاربر 

class NotificationPageAPIView (APIView) : 
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="صفحه اعلانات پنل کاربر"
    )
    def get(self,request) :
        notifications = Notification.objects.filter(user=request.user).union(Notification.objects.filter(send_to_all=True))

        paginator = Paginator(notifications.order_by("-created"),7)

        try : 
            result = paginator.page(request.GET.get("page",1))
        except EmptyPage : 
            result = paginator.page(1)
        except PageNotAnInteger : 
            result = paginator.page(1)

        data = {
            "notifications" : NotificationSerializer(result,many=True,context={'request':request}).data,
            "page" : NotificationPageSerializer(NotificationPage.objects.first()).data ,
            "count" : paginator.count,
            "page_nums" : paginator.num_pages,
            "next_page" : f"{request.build_absolute_uri().split("?")[0]}?page={result.next_page_number()}" 
            if result.has_next() else None,
            "previous_page" : f"{request.build_absolute_uri().split("?")[0]}?page={result.previous_page_number()}"
            if result.has_previous() else None,
        }
        return Response(data,status.HTTP_200_OK)
    
class ReadNotificationAPIView (APIView) : 

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="خواندن اعلان"
    )
    def post(self,request,notification_id) : 
        try :
            object = Notification.objects.get(id=notification_id)
        except : 
            return Response({'detail' : 'object not found .'},status.HTTP_404_NOT_FOUND)
        object.read_users.add(request.user)
        return Response({"message": "notification is readed ."})