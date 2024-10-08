from rest_framework import serializers
from project.models import Category,Project,ProjectImage,Comment,ProjectsPage
import re
from rest_framework.exceptions import ValidationError
from django_jalali.serializers.serializerfield import JDateField


# کلاس دسته بندی
class CategorySerializer(serializers.ModelSerializer) :

    class Meta :
        model = Category
        fields = ["id","name","slug","cover"] 


# کلاس تصاویر پروژه
class ProjectImageSerializer(serializers.ModelSerializer) :

    class Meta :
        model = ProjectImage
        fields = ["id","image"]

# کلاس پاسخ به کامنت
class ReplyCommentSerializer(serializers.ModelSerializer) :

    class Meta :
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "reply_to" : {"required" : True}
        }
    
    def validate(self, attrs):
        if not phone_regex.findall(attrs["phone"]) : 
            raise ValidationError({'phone' : 'invalid phone number .'})
        return super().validate(attrs)

# کلاس کامنت

phone_regex = re.compile("^0[0-9]{10}$")

class CommentSendSerializer(serializers.ModelSerializer) :

    class Meta :
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "phone" : {'required' : True},
            "email" : {"required" : True}
        }

    def to_representation(self,instance,**kwargs):
        context = super().to_representation(instance,**kwargs)
        context["replys"] = ReplyCommentSerializer(
            instance.replys.all(),
            many=True
        ).data
        return context
    
    def validate(self, attrs):
        if not phone_regex.findall(attrs["phone"]) : 
            raise ValidationError({'phone' : 'invalid phone number .'})
        return super().validate(attrs)


# کلاس پروژه
class ProjectSerializer(serializers.ModelSerializer) :

    launch_date = JDateField()

    JDateField = JDateField()

    class Meta :
        model = Project
        fields = "__all__"

    def to_representation(self,instance,**kwargs):
        context = super().to_representation(instance,**kwargs)
        context["images"] = ProjectImageSerializer(
            instance.images.all(),
            many=True,
            context=self.context
        ).data

        context["comments"] = CommentSendSerializer(
            instance.comments.filter(reply_to=None,is_valid=True),
            many=True
        ).data

        context["category"] = CategorySerializer(instance.category,context=self.context).data
        return context




# مدل ساده پروژه ها 
class ProjectSimpleSerializer (serializers.ModelSerializer) : 

    class Meta :  
        model = Project
        exclude = ["video","category"]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["image"] = ProjectImageSerializer(instance.images.first(),context=self.context).data
        context["cateogry"] = CategorySerializer(instance.category,context=self.context).data
        return context
    
# مدل صفحه پروژه ها
class ProjectsPageSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = ProjectsPage
        exclude = ["id"]