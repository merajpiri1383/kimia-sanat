from django.urls import path
from ticket.api import views



urlpatterns = [

    path("",views.TicketListCreateAPIView.as_view(),name="list-create-ticket"),

    path("search/",views.SearchTicketAPIView.as_view(),name="search"),

    path("<ticket_id>/",views.TicketDetailAPIView.as_view(),name="ticket-detail"),

    path("<ticket_id>/send-feedback/",views.SendFeedbackAPIView.as_view(),name="send-feedback"),

]