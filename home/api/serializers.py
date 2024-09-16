from rest_framework import serializers
from home.models import Slider,ImageSlider,License


# مدل تصاویر اسلایر ها
class ImageSliderSerializer (serializers.ModelSerializer) : 
    
    class Meta : 
        model = ImageSlider
        exclude = ["id","company"]




class SliderSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = Slider 
        exclude = ["id"]
    
    def to_representation(self,instance,**kwargs) : 
        context = super().to_representation(instance,**kwargs)
        context["sliders"] = ImageSliderSerializer(
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