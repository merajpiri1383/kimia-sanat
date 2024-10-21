from rest_framework import serializers
from template.models import (Footer,FooterLink,PhoneFooter,Header,
                    Menu,SubMenu,CategoryFooter,CommingSoon,BlogTitle,ProjectTitle,Comment,
                    AchievementCardItem,AchievementCard,AnswerQuestionTitle,ProductTitle,
                    FirstPageContent,Consult,ElectroLicense,Slider,PhoneAnswerQuestion,Achievement,AchievementTitle,
                    FooterFeq , CompanyCard,CompanyCardsPage)
from blog.api.serializers import BlogSimpleSerializer
from project.api.serializers import CategorySerializer as ProjectCategorySerializer
from product.api.serializers import CategorySerializer as ProductCategorySerializer 
import re
from rest_framework.exceptions import ValidationError

# مدل فوتر 

class CategoryFooterSerializer (serializers.ModelSerializer) : 
    class Meta : 
        model = CategoryFooter
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


class FooterFeqSerializer ( serializers.ModelSerializer ) : 
    class Meta : 
        model = FooterFeq
        exclude = ["id","footer"] 

class FooterSerializer (serializers.ModelSerializer) : 

    phones_fax = serializers.SerializerMethodField("get_phones_fax")

    phones_constant = serializers.SerializerMethodField("get_phones_constant")

    def get_phones_fax (self,obj) : 
        return FooterPhoneSerializer(obj.phones.filter(is_fax=True),many=True).data
    
    def get_phones_constant (self,obj) : 
        return FooterPhoneSerializer(obj.phones.filter(is_constant=True),many=True).data

    links = FooterLinkSerializer(many=True)

    categories = CategoryFooterSerializer(many=True)

    licenses = ElectroLicenseSerializer(many=True)

    feqs = FooterFeqSerializer(many=True)

    class Meta : 
        model = Footer
        exclude = ["id"]


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


# دستاورد 
class AchievementTitleSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = AchievementTitle
        exclude = ["id"]

class AchievementSerializer (serializers.ModelSerializer) :
    class Meta : 
        model = Achievement
        exclude = ["card","id"]


# مدال صفحه اول

 
class FirstPageSerilizer (serializers.ModelSerializer) : 

    achievements = AchievementSerializer(many=True)

    class Meta : 
        model = FirstPageContent
        exclude = ["id"]

    

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
    
# صفحه شماره کارت های شرکت 

class CardNumberSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = CompanyCard
        exclude = ["id","page"]

class CardNumbersPageSerializer (serializers.ModelSerializer) : 

    cards = CardNumberSerializer(many=True)

    class Meta : 
        model = CompanyCardsPage
        exclude = ["id"]