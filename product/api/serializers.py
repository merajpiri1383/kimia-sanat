from rest_framework import serializers
from product.models import (Product,Category,ImageProduct,Comment,Standard
            ,FeatureProduct,UsageProduct,ViolationComment)
from rest_framework.exceptions import ValidationError


# مدل تصویر

class ProductImageSerializer (serializers.ModelSerializer) :
    class Meta :
        model = ImageProduct
        fields = ["image"]

# مشخصات محصول 
class FeatureProductSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = FeatureProduct
        exclude = ["product"]

# کاربرد های محصول 
class UsageProductSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = UsageProduct
        exclude = ["product"]


# مدل استاندارد
class StandardSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = Standard
        fields = "__all__"


# مدل دسته بندی های محصول
class CategorySerializer (serializers.ModelSerializer) :

    class Meta :
        model = Category
        fields = "__all__"
        ref_name = "product category"

    def to_representation(self,instance) : 
        context = super().to_representation(instance)
        context["count_products"] = instance.products.count()
        return context

# مدل پاسخ کامنت
class CommentReplySerializer (serializers.ModelSerializer) :

    class Meta :
        model = Comment
        exclude = ["liked_by","disliked_by"]
        extra_kwargs = {
            "reply_to" : {"required" : True},
            "email" : {"required" : True}
        }
    
    def to_representation(self,instance,**kwargs) : 
        context = super().to_representation(instance,**kwargs)
        context["replys"] = CommentReplySerializer(instance.replys.all(),many=True).data
        context["reply_to"] = instance.reply_to.name if hasattr(instance.reply_to,'name') else None
        return context
# مدل کامنت

import re
phone_regex = re.compile("^0[0-9]{10}$") 

class CommentSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Comment
        exclude = ["reply_to","liked_by","disliked_by"]
        extra_kwargs = {
            "phone" : {"required" : True}
        }

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["replys"] = CommentReplySerializer(instance.replys.all(),many=True).data
        context["like_count"] = instance.liked_by.count()
        context["dislike_count"] = instance.disliked_by.count()
        context["reply_to"] = instance.reply_to.name if hasattr(instance.reply_to,"name") else None
        return context


# مدل ساده محصول
class ProductSimpleSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Product
        fields = ["id","slug","title","image","type","code","description"]

    def to_representation(self, instance,**kwargs):
        context = super().to_representation(instance,**kwargs)
        context["views"] = instance.views.count()
        context["category"] = CategorySerializer(instance.category).data
        context["liked_by_user"] = self.context["request"].user in instance.liked.all()
        context["like_count"] = instance.liked.count()
        return context


#  مدل محصول به همراه جزییات

class ProductSerializer (serializers.ModelSerializer) :

    category = CategorySerializer()

    standard = StandardSerializer(many=True)

    usages = UsageProductSerializer(many=True)

    features = FeatureProductSerializer(many=True)

    images = ProductImageSerializer(many=True)

    comments = serializers.SerializerMethodField(method_name="get_comments")

    def get_comments (self,instance) : 
        return CommentSerializer(instance.comments.filter(reply_to=None),many=True).data

    class Meta :
        model = Product
        exclude = ["views","liked"]

    def to_representation(self,instance,**kwargs):
        context = super().to_representation(instance,**kwargs)
        context["views"] = instance.views.count()
        context["liked_by_user"] = self.context["request"].user in instance.liked.all()
        context["like_count"] = instance.liked.count()
        context["related_products"] = ProductSimpleSerializer(
            instance.category.products.exclude(id=instance.id).order_by("-created")[:6],
            many=True, 
            context=self.context
        ).data
        return context

    
# مدل گزارش تخلف کامنت

class ViolationCommentSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = ViolationComment 
        fields = "__all__"
        ref_name = "product_comment_violation"