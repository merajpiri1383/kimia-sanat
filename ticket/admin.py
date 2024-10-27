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
    list_display = ["index","number","get_name","title","status"]
    ordering = ["created"]

    def index (self,obj) : 
        return list(Ticket.objects.all().order_by("-created")).index(obj) + 1
    index.short_description = "ردیف"

    def get_name (self,obj) :
        if obj.is_from_admin : 
            return "ادمین"
        else : 
            if hasattr(obj.user,"real_profile") : 
                return obj.user.real_profile.name
            elif hasattr(obj.user,"legal_profile") : 
                return obj.user.legal_profile.name 
    get_name.short_description = "نام کاربر"