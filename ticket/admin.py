from django.contrib import admin
from ticket.models import Ticket,TicketFile


# مدل تیکت

class TicketFileInline (admin.TabularInline) : 
    model = TicketFile
    exclude = ["id"]
    extra = 0

@admin.register(Ticket)
class TicketAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [TicketFileInline]