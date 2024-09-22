from rest_framework import serializers
from project.models import Category,Project,ProjectImage,Comment,ProjectsPage


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
        fields = ["id","project","reply_to","name","text"]
        extra_kwargs = {
            "reply_to" : {"required" : True}
        }

# کلاس کامنت
class CommentSendSerializer(serializers.ModelSerializer) :

    class Meta :
        model = Comment
        fields = ["id","project","name","phone","email","text","created"]
        extra_kwargs = {
            "phone" : {'required' : True},
            "email" : {"required" : True}
        }

    def to_representation(self,instance,**kwargs):
        context = super().to_representation(instance,**kwargs)
        context["replys"] = ReplyCommentSerializer(
            instance.relpys.all(),
            many=True
        ).data
        return context


# کلاس پروژه
class ProjectSerializer(serializers.ModelSerializer) :

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
        return context




# مدل ساده پروژه ها 
class ProjectSimpleSerializer (serializers.ModelSerializer) : 

    class Meta :  
        model = Project
        fields = ["id","name","description","contractor","launch_date","start_date"]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["image"] = ProjectImageSerializer(instance.images.first(),context=self.context).data
        return context
    
# مدل صفحه پروژه ها
class ProjectsPageSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = ProjectsPage
        exclude = ["id"]