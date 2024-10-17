from rest_framework import serializers
from notification.models import Notification,NotificationPage


# مدیرت صفحه اعلانات
class NotificationPageSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = NotificationPage
        exclude = ["id"]



# اعلان 
class NotificationSerializer (serializers.ModelSerializer) : 

    is_read = serializers.SerializerMethodField("get_is_read")

    def get_is_read (self,obj) : 
        return self.context["request"].user in obj.read_users.all()
    
    class Meta : 
        model = Notification
        exclude = ["send_to_all","user","read_users"]