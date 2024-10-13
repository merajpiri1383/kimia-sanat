from ticket.models import Ticket,TicketFile
from rest_framework import serializers

# تیکت
class TicketSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = Ticket
        fields = "__all__"
    
    def __init__(self,instance=None,**kwargs) :
        if instance : 
            kwargs["partial"] = True
        return super().__init__(instance,**kwargs) 