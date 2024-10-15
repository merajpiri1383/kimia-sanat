from ticket.models import Ticket,TicketFile,Feedback
from rest_framework import serializers



# فایل های تیکت
class TicketFileSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = TicketFile
        exclude = ["ticket"]


# فیدبک

class FeedbackSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = Feedback 
        exclude = ["id","ticket"]


# رپلای تیکت 

class ReplyTicketSerializer (serializers.ModelSerializer) : 

    files = TicketFileSerializer(many=True,required=False)

    feedback = FeedbackSerializer()

    class Meta : 
        model = Ticket
        exclude = ["reply_to"]

# تیکت
class TicketSerializer (serializers.ModelSerializer) : 

    files = TicketFileSerializer(many=True,required=False)

    replys = ReplyTicketSerializer(many=True)

    feedback = FeedbackSerializer()

    class Meta : 
        model = Ticket
        exclude = ["reply_to"]
    
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