from rest_framework import serializers
from template.models import (Footer,FooterLink,PhoneFooter,SocialFooter,Header,
                    Menu,SubMenu,CategoryFooter,CommingSoon,BlogTitle,ProjectTitle,Comment,
                    AchievementCardItem,AchievementCard,AnswerQuestionTitle,ProductTitle,
                    FirstPageContent,Consult,ElectroLicense,Slider,PhoneAnswerQuestion,Achievement,AchievementTitle)
from blog.api.serializers import BlogSimpleSerializer
from project.api.serializers import CategorySerializer as ProjectCategorySerializer
from product.api.serializers import CategorySerializer as ProductCategorySerializer 
import re
from rest_framework.exceptions import ValidationError

# مدل فوتر 

class CategoryFooter (serializers.ModelSerializer) : 
    class Meta : 
        model = CategoryFooter
        exclude = ["id","footer"]

class SocialFooterSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model =SocialFooter
        exclude = ["id","footer"]

class FooterPhoneSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = PhoneFooter
        exclude = ["id","footer"]

class FooterLinkSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = FooterLink
        exclude = ["id","footer"]

class ElectroLicenseSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = ElectroLicense
        exclude = ["id","footer"]

class FooterSerializer (serializers.ModelSerializer) : 


    class Meta : 
        model = Footer
        exclude = ["id"]

    def to_representation(self,instance,**kwargs) : 
        context = super().to_representation(instance,**kwargs)
        context["phones"] = FooterPhoneSerializer(instance.footer_phones.all(),many=True,context=self.context).data
        context["links"] = FooterLinkSerializer(instance.footer_links.all(),many=True,context=self.context).data
        context["socials"] = SocialFooterSerializer(instance.footer_socials.all(),many=True,context=self.context).data
        context["categories"] = CategoryFooter(instance.footer_category.all(),many=True,context=self.context).data
        context["licenses"] = ElectroLicenseSerializer(instance.licenses.all(),many=True,context=self.context).data
        return context


# مدل هدر 

class SubMenuSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = SubMenu
        exclude = ["id","menu"]

class MenuSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = Menu
        exclude = ["id","header"]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["sub_menus"] = SubMenuSerializer(instance.sub_menus.all(),many=True).data
        return context

class HeaderSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = Header
        exclude = ["id"]
    
    def to_representation(self, instance):
        context = super().to_representation(instance)
        context["menus"] = MenuSerializer(instance.menus.all(),many=True).data
        return context
    
# comming soon

class CommingSoonSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = CommingSoon
        exclude = ["id"]



# کادر بلاگ در صفحه اصلی
class BlogTtileSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = BlogTitle
        exclude = ["id","blogs"]
    
    def to_representation(self,instance,**kwargs) : 
        context = super().to_representation(instance,**kwargs)
        context["blogs"] = BlogSimpleSerializer(instance.blogs.all(),many=True,context=self.context).data
        return context
    

# مدل کادر پروژه ها

class CommentProjectSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = Comment
        exclude = ["id","project"]

class ProjectTitleSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = ProjectTitle
        exclude = ["id","category_projects"]

    def to_representation(self,instance,**kwargs) :
        context = super().to_representation(instance,**kwargs)
        context["categories"] = ProjectCategorySerializer(
            instance.category_projects.all(),
            many=True,
            context=self.context
        ).data
        context["comments"] = CommentProjectSerializer(instance.comments.all(),many=True,context=self.context).data
        return context
    
# مدل دستاورد ها

class AchievementCardItemSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = AchievementCardItem
        exclude = ["id","achievement"]

class AchievementCardSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = AchievementCard
        exclude = ["id"]

    def to_representation(self,instance) : 
        context = super().to_representation(instance)
        context["items"] = AchievementCardItemSerializer(
            instance.items.all(),
            many=True
        ).data
        return context
    

# مدل پاسخ به سوالات مشتری

class PhoneAnswerSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = PhoneAnswerQuestion
        exclude = ["card","id"]

class AnswerQuestionTitleSerializer (serializers.ModelSerializer) : 

    phones = PhoneAnswerSerializer(many=True)
    
    class Meta : 
        model = AnswerQuestionTitle
        exclude = ["id"]

# کادر محصول
class ProductTitleSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = ProductTitle
        exclude = ["id"]

    def to_representation(self,instance,**kwargs) :
        context = super().to_representation(instance,**kwargs)
        context["categories"] = ProductCategorySerializer(
            instance.categories.all(),
            many=True,
            context=self.context
        ).data
        return context


# اسلایدر 


class SliderSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = Slider
        exclude = ["id"]


# مدال صفحه اول

 
class FirstPageSerilizer (serializers.ModelSerializer) : 

    # licenses = LicenseSerializer(many=True)

    class Meta : 
        model = FirstPageContent
        exclude = ["id"]
    

# دستاورد 
class AchievementTitleSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = AchievementTitle
        exclude = ["id"]

class AchievementSerializer (serializers.ModelSerializer) :
    class Meta : 
        model = Achievement
        exclude = ["card","id"]
    

# مدل درخواست مشاوره
regex_phone = re.compile("^0[0-9]{10}$")

class ConsultSerializer (serializers.ModelSerializer) : 
    
    class Meta : 
        model = Consult
        fields = "__all__"
    
    def validate(self,attrs) : 

        if not regex_phone.findall(attrs["phone"]) : 
            raise ValidationError({'phone' : 'invalid phone number .'})
        return super().validate(attrs) 