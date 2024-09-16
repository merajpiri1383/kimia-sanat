from rest_framework import serializers
from product.models import (Product,Category,Standard,FeatureProduct,UsageProduct
            ,ImageProduct,Comment)


# مدل تصویر

class ProductImageSerializer (serializers.ModelSerializer) :
    class Meta :
        model = ImageProduct
        fields = ["image"]

# مدل دسته بندی های محصول
class CategorySerializer (serializers.ModelSerializer) :

    class Meta :
        model = Category
        fields = ["name","slug","icon","description"]

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


#  مدل محصول به همراه جزییات

class ProductSerializer (serializers.ModelSerializer) :
    class Meta :
        model = Product
        exclude = ["id","tags","views"]

    def to_representation(self,instance,**kwargs):
        context = super().to_representation(instance,**kwargs)
        context["views"] = instance.views.count()
        context["images"] = ProductImageSerializer(
            instance.images.all(),
            many=True,
            context=self.context
        ).data
        context["category"] = CategorySerializer(instance.category).data
        return context



# مدل ساده محصول
class ProductSimpleSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Product
        fields = ["id","slug","title","type","code","description"]

    def to_representation(self, instance,**kwargs):
        context = super().to_representation(instance,**kwargs)
        context["image"] = ProductImageSerializer(
            instance.images.first(),
            context=self.context
        ).data
        context["views"] = instance.views.count()
        context["category"] = CategorySerializer(instance.category).data
        return context


