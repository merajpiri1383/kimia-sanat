from rest_framework import serializers
from template.models import (Footer,FooterLink,PhoneFooter,SocialFooter,Header,Menu,SubMenu,CategoryFooter)

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