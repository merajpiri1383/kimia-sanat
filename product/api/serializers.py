from rest_framework import serializers
from product.models import (Product,Category,ImageProduct,Comment,Count,Standard)


# مدل تصویر

class ProductImageSerializer (serializers.ModelSerializer) :
    class Meta :
        model = ImageProduct
        fields = ["image"]

# مدل استاندارد
class StandardSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = Standard
        fields = "__all__"


# مدل دسته بندی های محصول
class CategorySerializer (serializers.ModelSerializer) :

    class Meta :
        model = Category
        fields = ["name","slug","icon","description"]

    def to_representation(self,instance) : 
        context = super().to_representation(instance)
        context["count_products"] = instance.products.count()
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
    
# مدل مقدار محصول
class CountSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Count
        exclude = ["product"]
    
    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["product"] = {
            'id' : instance.product.id,
            'name' : instance.product.title
        }
        return context


#  مدل محصول به همراه جزییات

class ProductSerializer (serializers.ModelSerializer) :

    standard = StandardSerializer(many=True)

    class Meta :
        model = Product
        exclude = ["id","views","liked"]

    def to_representation(self,instance,**kwargs):
        context = super().to_representation(instance,**kwargs)
        context["views"] = instance.views.count()
        context["liked_by_user"] = self.context["request"].user in instance.liked.all()
        context["like_count"] = instance.liked.count()
        context["images"] = ProductImageSerializer(
            instance.images.all(),
            many=True,
            context=self.context
        ).data
        context["counts"] = CountSerializer(
            instance.counts.all(),
            many=True
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
        context["liked_by_user"] = self.context["request"].user in instance.liked.all()
        context["like_count"] = instance.liked.count()
        return context
