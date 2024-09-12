from rest_framework import serializers
from blog.models import Blog,Module,Category

# مدل ماژول
class ModuleSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Module
        fields = "__all__"


# مدل بلاگ
class BlogSerializer (serializers.ModelSerializer) :

    class Meta :
        model = Blog
        fields = "__all__"


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