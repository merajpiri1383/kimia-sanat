from django.contrib import admin
from template.models import (
    CommingSoon,
    LoginPage,
    LoginPageSlide
)
from jalali_date.admin import ModelAdminJalaliMixin

from template.panel.admin import *
from template.main.admin import *
from template.header.admin import *
from template.footer.admin import *

# مدیرت Comming Soon
@admin.register(CommingSoon) 
class CommingSoonAdminModel (ModelAdminJalaliMixin,admin.ModelAdmin) : 
    exclude = ["id"]


# login page 

class LoginPageSlideInline (admin.TabularInline) : 
    model = LoginPageSlide
    exclude = ["id"]
    extra = 0

@admin.register(LoginPage)
class LoginPageAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [LoginPageSlideInline]