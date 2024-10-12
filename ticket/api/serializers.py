from ticket.models import Ticket,TicketFile
from rest_framework import serializers

# فایل های تیکت

class TicketFileSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = TicketFile
        exclude = ["ticket"]

# تیکت
class TicketSerializer (serializers.ModelSerializer) : 

    file = serializers.ListField(
        child=serializers.FileField(),
        required=False
    )

    # def create(self, validated_data):
    #     files = validated_data.pop('files')
    #     file_instances = [TicketFile(file=file) for file in files]
    #     return TicketFile.objects.bulk_create(file_instances)

    class Meta : 
        model = Ticket
        fields = "__all__"
    
    def __init__(self,instance=None,**kwargs) :
        if instance : 
            kwargs["partial"] = True
        return super().__init__(instance,**kwargs) 