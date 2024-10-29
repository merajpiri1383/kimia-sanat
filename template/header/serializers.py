from rest_framework import serializers
from template.header.models import (
    Header,
    Menu,
    SubMenu
)


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