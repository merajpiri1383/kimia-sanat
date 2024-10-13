from django.contrib import admin
from ticket.models import Ticket


# مدل تیکت

@admin.register(Ticket)
class TicketAdmin (admin.ModelAdmin) : 
    exclude = ["id"]