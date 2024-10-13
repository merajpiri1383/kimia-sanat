from ticket.models import Ticket,TicketFile
from rest_framework.exceptions import ValidationError
from rest_framework import serializers



# فایل های تیکت
class TicketFileSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = TicketFile
        exclude = ["ticket"]


# تیکت
class TicketSerializer (serializers.ModelSerializer) : 

    files = TicketFileSerializer(many=True,required=False)

    class Meta : 
        model = Ticket
        fields = "__all__"
    
    def __init__(self,instance=None,**kwargs) :
        if instance : 
            kwargs["partial"] = True
        return super().__init__(instance,**kwargs) 
    
    def create(self,validated_data) : 
        
        ticket = Ticket.objects.create(**validated_data)
        try : 
            files = self.context["request"].FILES.getlist("files")
            for file in files : 
                TicketFile.objects.create(
                    ticket = ticket , 
                    file = file 
                )
        except : pass 
        return ticket