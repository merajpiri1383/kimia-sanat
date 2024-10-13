from django.contrib import admin
from ticket.models import Ticket,TicketFile


# مدل تیکت

class TicketInline (admin.StackedInline) : 
    model = Ticket
    extra = 0
    exclude = ["id"]

class TicketFile (admin.TabularInline) : 
    model = TicketFile
    extra = 0
    exclude =["id"]

@admin.register(Ticket)
class TicketAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [TicketInline,TicketFile]