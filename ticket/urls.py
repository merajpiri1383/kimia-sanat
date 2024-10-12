from django.urls import path
from ticket.api import views



urlpatterns = [

    path("",views.TicketListCreateAPIView.as_view(),name="list-create-ticket"),

    path("<ticket_id>/",views.TicketDetailAPIView.as_view(),name="ticket-detail")

]