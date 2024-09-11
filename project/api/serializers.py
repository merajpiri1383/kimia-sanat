from rest_framework import serializers
from project.models import Category,Project,ProjectImage


# کلاس دسته بندی
class CategorySerializer(serializers.ModelSerializer) :

    class Meta :
        model = Category
        fields = ["id","name","cover"]


# کلاس تصاویر پروژه
class ProjectImageSerializer(serializers.ModelSerializer) :

    class Meta :
        model = ProjectImage
        fields = ["id","image"]


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
        return context