from ticket.models import Ticket,TicketFile,Feedback
from rest_framework import serializers
from user.models import RealProfile,LegalProfile


class SimpleRealProfileSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = RealProfile
        fields = ["name","profile_image"]

class SimpleLegalProfileSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = LegalProfile
        fields = ["name","profile_image"]



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

    replys = ReplyTicketSerializer(many=True,read_only=True,required=False)

    feedback = FeedbackSerializer(read_only=True,required=False)

    user = serializers.SerializerMethodField("get_user")

    def get_user(self,obj) : 
        if hasattr(obj.user,"real_profile") : 
            return SimpleRealProfileSerializer(obj.user.real_profile,context=self.context).data
        elif hasattr(obj.user,"legal_profile") : 
            return SimpleLegalProfileSerializer(
                obj.user.legal_profile,
                context=self.context
            ).data

    class Meta : 
        model = Ticket
        exclude = ["reply_to"]
        read_only_fields = ["id","is_from_admin","created","number","status"]
    
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
    
    def update(self, instance, validated_data):
        files = self.context["request"].FILES.getlist("files")
        if len(files) > 0 : 
            for file in instance.files.all() : 
                file.delete()
            for file in files : 
                TicketFile.objects.create(
                    ticket = instance , 
                    file = file 
                )
        return super().update(instance, validated_data)