from rest_framework import serializers
from project.models import Category,Project,ProjectImage,Comment,ProjectsPage,VideoProject,ViolationComment
import re
from rest_framework.exceptions import ValidationError


# کلاس دسته بندی
class CategorySerializer(serializers.ModelSerializer) :

    class Meta :
        model = Category
        fields = ["id","name","slug","cover"] 


# کلاس تصاویر پروژه
class ProjectImageSerializer(serializers.ModelSerializer) :

    class Meta :
        model = ProjectImage
        fields = ["image"]

# کلاس ویدیو های پروژه 
class VideoProjectSerializer (serializers.ModelSerializer) : 

    class Meta :
        model = VideoProject
        fields = ["video"]

# کلاس پاسخ به کامنت
class ReplyCommentSerializer(serializers.ModelSerializer) :

    class Meta :
        model = Comment
        exclude = ["liked_by","disliked_by"]
        extra_kwargs = {
            "reply_to" : {"required" : True}
        }

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["like_count"] = instance.liked_by.count()
        context["dislike_count"] = instance.disliked_by.count()
        return context
    
    def validate(self, attrs):
        if not phone_regex.findall(attrs["phone"]) : 
            raise ValidationError({'phone' : 'invalid phone number .'})
        return super().validate(attrs)

# کلاس کامنت

phone_regex = re.compile("^0[0-9]{10}$")

class CommentSendSerializer(serializers.ModelSerializer) :

    class Meta :
        model = Comment
        exclude = ["reply_to","liked_by","disliked_by"]
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
        context["like_count"] = instance.liked_by.count()
        context["dislike_count"] = instance.disliked_by.count()
        return context
    
    def validate(self, attrs):
        if not phone_regex.findall(attrs["phone"]) : 
            raise ValidationError({'phone' : 'invalid phone number .'})
        return super().validate(attrs)


# کلاس پروژه
class ProjectSerializer(serializers.ModelSerializer) :

    category = CategorySerializer() 

    images = ProjectImageSerializer(many=True)

    videos = VideoProjectSerializer(many=True)

    class Meta :
        model = Project
        fields = "__all__"

    def to_representation(self,instance,**kwargs):
        context = super().to_representation(instance,**kwargs)

        context["comments"] = CommentSendSerializer(
            instance.comments.filter(reply_to=None,is_valid=True),
            many=True
        ).data
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
        # context["launch_date"] = date2jalali(instance.launch_date).strftime("%Y-%d-%m")
        # context["start_date"] = date2jalali(instance.start_date).strftime("%Y-%d-%m")
        return context 
    
# مدل صفحه پروژه ها
class ProjectsPageSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = ProjectsPage
        exclude = ["id"]

# مدل گزارش تخلف کامنت

class ViolationCommentSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = ViolationComment 
        fields = "__all__"
        ref_name = "project_comment_violation"