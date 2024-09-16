from rest_framework import serializers
from home.models import Company,Consult,ImageCompany,License


# مدل تصاویر اسلایر ها
class ImageCompanySerializer (serializers.ModelSerializer) : 
    
    class Meta : 
        model = ImageCompany
        exclude = ["id","company"]

# مدل شرکت
class CompanySerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = Company
        exclude = ["id"]
    
    def to_representation(self,instance,**kwargs) : 
        context = super().to_representation(instance,**kwargs)
        context["sliders"] = ImageCompanySerializer(
            instance.images.all(),
            many=True,
            context=self.context
        ).data
        return context
    
# مدل گواهی نامه ها
class LicenseSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = License
        fields = ["title","icon","description"]