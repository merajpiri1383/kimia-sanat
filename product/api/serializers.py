from rest_framework import serializers
from product.models import (Product,Category,ImageProduct,Comment,Count,Standard,FeatureProduct,UsageProduct)


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

    def to_representation(self,instance) : 
        context = super().to_representation(instance)
        context["count_products"] = instance.products.count()
        return context

# مدل پاسخ کامنت
class CommentReplySerializer (serializers.ModelSerializer) :

    class Meta :
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "reply_to" : {"required" : True}
        }
# مدل کامنت

class CommentSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Comment
        exclude = ["reply_to"]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["replys"] = CommentReplySerializer(instance.replys.all(),many=True).data
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


#  مدل محصول به همراه جزییات

class ProductSerializer (serializers.ModelSerializer) :

    category = CategorySerializer()

    standard = StandardSerializer(many=True)

    usages = UsageProductSerializer(many=True)

    features = FeatureProductSerializer(many=True)

    counts = CountSerializer(many=True)

    images = ProductImageSerializer(many=True)

    comments = serializers.SerializerMethodField(method_name="get_comments")

    def get_comments (self,instance) : 
        print(instance.comments.all())
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
            instance.category.products.all().order_by("-created")[:3],
            many=True, 
            context=self.context
        ).data
        return context