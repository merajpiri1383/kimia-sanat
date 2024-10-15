from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from ticket.models import Ticket
from ticket.api.serializers import TicketSerializer,FeedbackSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from ticket.permissions import FeedbackPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



# لیست تیکت ها

class TicketListCreateAPIView (APIView) : 

    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(
        operation_summary="لیست تیکت ها",
    )
    def get(self,request) : 

        paginator = Paginator(request.user.tickets.all(),per_page=5)
        try :
            tickets = paginator.page(request.GET.get("page",1))
        except EmptyPage : 
            tickets = paginator.page(1)
        except PageNotAnInteger : 
            tickets = paginator.page(1)
        data = {
            "tickets" : TicketSerializer(tickets,many=True,context={'request':request}).data,
            "count" : paginator.count ,
            "pages" : paginator.num_pages,
            "next_page" : f"{request.build_absolute_uri().split("?")[0]}?page={tickets.next_page_number()}" if tickets.has_next() else None,
            "previous_page" : f"{request.build_absolute_uri().split("?")[0]}?page={tickets.previous_page_number()}" if tickets.has_previous() else None
        }
        return Response(data,status.HTTP_200_OK)
    

    @swagger_auto_schema(
        operation_summary="ارسال تیکت",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title" : openapi.Schema(type=openapi.TYPE_STRING,description="عنوان"),
                "department" : openapi.Schema(type=openapi.TYPE_STRING,description="دپارتمان"),
                "text" : openapi.Schema(type=openapi.TYPE_STRING,description="توضیحات"),
            },
            required=["title","department","text"],
        ),
        responses={
            201 : TicketSerializer(),
            400 : "bad request"
        }
    )
    def post(self,request) : 
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = TicketSerializer(data=data,context={'request':request})
        if serializer.is_valid() : 
            ticket = serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        else : 
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        


# جزيات تیکت

class TicketDetailAPIView (APIView) : 

    permission_classes = [IsAuthenticated]

    def get_ticket (self,request,ticket_id) : 
        try : 
            self.ticket = Ticket.objects.get(id=ticket_id)
        except :
            return Response({'detail':"ticket not found ."},status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(
        operation_summary="جزيیات تیکت",
        responses={
            200 : TicketSerializer(),
            404 : "not found"
        }
    )
    def get(self,request,ticket_id) : 
        if self.get_ticket(request,ticket_id) : return self.get_ticket(request,ticket_id)
        serializer = TicketSerializer(self.ticket,context={"request":request})
        return Response(serializer.data,status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary="تغییر تیکت",
        operation_description="فقط درصورتی قابل تغییر هست که در وضعیت checking باشه",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title" : openapi.Schema(type=openapi.TYPE_STRING,description="عنوان"),
                "department" : openapi.Schema(type=openapi.TYPE_STRING,description="دپارتمان"),
                "text" : openapi.Schema(type=openapi.TYPE_STRING,description="توضیحات"),
            },
        ),
        responses={
            200 : TicketSerializer(),
            400 : "bad request"
        }
    )
    def put(self,request,ticket_id) : 
        if self.get_ticket(request,ticket_id) : return self.get_ticket(request,ticket_id)
        if not self.ticket.status == "checking" : 
            return Response({'detail':"ticket cant edit ."},status.HTTP_400_BAD_REQUEST)
        serializer = TicketSerializer(instance=self.ticket,data=request.data,context={'request':request})
        if serializer.is_valid() : 
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        else : 
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        

# ارسال بازخورد برای تیکت

class SendFeedbackAPIView (APIView) : 

    permission_classes = [IsAuthenticated,FeedbackPermission]

    @swagger_auto_schema(
        operation_summary="ارسال بازخورد",
        operation_description="""
                    type میتونه سه حالت داشته باشه 
                    1 good , 2 middle , 3 bad
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "type" : openapi.Schema(type=openapi.TYPE_STRING,description="نوع بازخورد"),
                "description" : openapi.Schema(type=openapi.TYPE_STRING,description="توضیحات"),
            },
            required=["type","description"]
        ),
    )
    def post(self,request,ticket_id) : 
        try : 
            ticket = Ticket.objects.get(id=ticket_id)
        except : 
            return Response({'detail':'ticket not found .'},status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request,ticket)
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = FeedbackSerializer(data=data)
        if serializer.is_valid() : 
            instance = serializer.save()
            instance.ticket = ticket
            instance.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else : 
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)