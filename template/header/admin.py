from django.contrib import admin
from template.models import (
    Menu,
    SubMenu,
    Header
)

from nested_inline.admin import NestedStackedInline, NestedModelAdmin


# مدل هدر 

class SubMenuTabular (NestedStackedInline) : 
    model = SubMenu
    extra = 0
    exclude = ["id"]
    fk_name = "menu"

class MenuInline (NestedStackedInline) : 
    exclude = ["id"]
    model = Menu
    extra = 0
    fk_name = 'header'
    inlines = [SubMenuTabular]

@admin.register(Header) 
class HeaderAdmin (NestedModelAdmin) : 
    exclude = ["id"]
    inlines = [MenuInline]