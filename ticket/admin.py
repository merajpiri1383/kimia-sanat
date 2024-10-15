from django.contrib import admin
from ticket.models import Ticket,TicketFile,Feedback


# مدل تیکت

class FeedbackInline (admin.StackedInline) : 
    model = Feedback
    extra = 0
    exclude = ["id"]

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
    inlines = [TicketInline,TicketFile,FeedbackInline]