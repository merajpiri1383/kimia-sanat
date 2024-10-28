from rest_framework import serializers
from blog.models import Blog,Module,Category,Comment,Tag,ViolationComment
from rest_framework.exceptions import ValidationError


# مدل برچسب 
class TagSerializer (serializers.ModelSerializer) : 
    
    class Meta : 
        model = Tag
        fields = "__all__"

# مدل ماژول
class ModuleSerializer (serializers.ModelSerializer) : 

    class Meta :
        model = Module
        exclude = ["blog","created"]


# مدل بلاگ
class BlogSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Blog
        exclude = ["user_waiting"]
    
    def to_representation(self,instance,**kwargs) : 
        context = super().to_representation(instance,**kwargs)
        context["content"] = ModuleSerializer(
            instance.modules.all(),
            many=True,
            context=self.context
        ).data
        context["tag"] = TagSerializer(instance.tag.all(),many=True).data
        return context


# مدل ساده بلاگ برای لیست
class BlogSimpleSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Blog
        exclude = ["user_waiting"]

    def to_representation(self, instance,**kwargs):
        context = super().to_representation(instance,**kwargs)
        context["category"] = {
            "id" : instance.category.id,
            "name" : instance.category.name,
            "slug" : instance.category.slug
        }
        context["tag"] = TagSerializer(instance.tag.all(),many=True).data
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
        exclude = ["liked_by","disliked_by"]
        extra_kwargs = {
            "reply_to" : {"required" : True}
        }

# مدل کامنت

import re
phone_regex = re.compile("^0[0-9]{10}$") 

class CommentSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Comment
        exclude = ["reply_to","liked_by","disliked_by"]
        read_only_fields = ["liked_by","disliked_by","is_from_admin"]
        extra_kwargs = {
            "phone" : {"required" : True}
        }

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["replys"] = CommentReplySerializer(instance.replys.all(),many=True).data
        context["like_count"] = instance.liked_by.count()
        context["dislike_count"] = instance.disliked_by.count()
        return context
    
    def validate(self, attrs):
        if not phone_regex.findall(attrs["phone"]) : 
            raise ValidationError({'phone':'invalid phone'})
        return super().validate(attrs)
    

# مدل گزارش تخلف کامنت

class ViolationCommentSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = ViolationComment 
        fields = "__all__"
        ref_name = "blog_comment_violation"