from rest_framework import serializers
from blog.models import Blog,Module,Category,Comment,BlogsPage

# مدل ماژول
class ModuleSerializer (serializers.ModelSerializer) : 

    class Meta :
        model = Module
        exclude = ["blog","created"]


# مدل بلاگ
class BlogSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Blog
        fields = "__all__"
    
    def to_representation(self,instance,**kwargs) : 
        context = super().to_representation(instance,**kwargs)
        context["content"] = ModuleSerializer(
            instance.modules.all(),
            many=True,
            context=self.context
        ).data
        return context


# مدل ساده بلاگ برای لیست
class BlogSimpleSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Blog
        fields = "__all__"

    def to_representation(self, instance,**kwargs):
        context = super().to_representation(instance,**kwargs)
        context["category"] = {
            "id" : instance.category.id,
            "name" : instance.category.name
        }
        return context

# مدل دسته بندی
class CategorySerializer (serializers.ModelSerializer) :

    class Meta :
        model = Category
        fields = "__all__"

    def to_representation(self, instance,**kwargs):
        context = super().to_representation(instance,**kwargs)
        context["blog_count"] = instance.blogs.count()
        return context
    


# مدل پاسخ کامنت
class CommentReplySerializer (serializers.ModelSerializer) :

    class Meta :
        model = Comment
        exclude = ["created"]
        extra_kwargs = {
            "reply_to" : {"required" : True}
        }

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["created_date"] = instance.created.strftime("%Y-%m-%d")
        context["created_time"] = instance.created.strftime("%H:%M:%S")
        return context

# مدل کامنت

class CommentSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Comment
        exclude = ["reply_to","created"]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["replys"] = CommentReplySerializer(instance.replys.all(),many=True).data
        context["created_date"] = instance.created.strftime("%Y-%m-%d")
        context["created_time"] = instance.created.strftime("%H:%M:%S")
        return context
    

# مدل صفحه بلاگ
class BlogsPageSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = BlogsPage
        exclude = ["id"]