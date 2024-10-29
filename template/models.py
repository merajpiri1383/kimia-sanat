from django.db import models
from uuid import uuid4
from django_jalali.db.models import jDateTimeField
from template.panel.models import *
from template.header.models import *
from template.footer.models import *
from template.main.models import *


# مدل کامینگ سون
class CommingSoon (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    logo = models.ImageField(upload_to="template/commingsoon/logo/",verbose_name="لوگو",null=True,blank=True)

    title = models.CharField(max_length=256,verbose_name="عنوان صفحه",null=True,blank=True)

    sub_title = models.CharField(max_length=256,blank=True,null=True,verbose_name="زیر عنوان")

    background_image = models.ImageField(upload_to="template/commingsoon/",verbose_name="بک گراند صفحه",null=True,blank=True)

    time = jDateTimeField(null=True,blank=True,verbose_name="زمان")

    copy_right_text = models.TextField(null=True,blank=True,verbose_name="متن کپی رایت")

    is_active = models.BooleanField(default=False,verbose_name="فعال است")

    def __str__(self) : 
        return "صفحه comming soon"
    
    class Meta : 
        verbose_name = "Comming Soon"
        verbose_name_plural = "مدیرت Comming Soon"


# صفحه لاگین
class LoginPage (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    logo = models.ImageField(
        upload_to="template/login",
        null=True,
        blank=True,
        verbose_name="لوگو"
    )

    text = models.CharField(
        max_length=450,
        null=True,
        blank=True,
        verbose_name="متن زیر دکمه"
    )

    def __str__ (self) : 
        return "صفحه لاگین"
    
    class Meta : 
        verbose_name = "صفحه لاگین"
        verbose_name_plural = "صفحه لاگین"


# اسلایدر صفحه لاگین

class LoginPageSlide (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    page = models.ForeignKey(
        to=LoginPage,
        on_delete=models.CASCADE,
        related_name="sliders",
    )

    image = models.ImageField(
        upload_to="template/login/slider/",
        verbose_name="تصویر"
    )

    def __str__ (self) : 
        return "اسلاید"
    
    class Meta : 
        verbose_name = "اسلاید"
        verbose_name_plural = "اسلاید ها"