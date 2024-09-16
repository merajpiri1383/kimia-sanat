from django.db import models
from django.core.exceptions import ValidationError
from uuid import uuid4
import re


regex_phone = re.compile("^0[0-9]{10}$")

class Company (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    title_slider = models.CharField(max_length=256,verbose_name="عنوان اسلایدر",null=True,blank=True)

    text_slider = models.TextField(null=True,blank=True,verbose_name="متن اسلایدر")

    short_description = models.TextField(null=True,blank=True,verbose_name="توضیحات مختصر و مفید")

    def __str__(self) : 
        return "شرکت"
    
    class Meta : 
        verbose_name = "شرکت"
        verbose_name_plural = "تنظمات صفحه هوم"



class ImageCompany (models.Model ) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    company = models.ForeignKey(
        to = Company,
        on_delete = models.CASCADE,
        related_name = "images"
    )

    image = models.ImageField(upload_to="company/images/",verbose_name="تصویر")

    def __str__ (self) : 
        return "image"
    
    class Meta : 
        verbose_name = "تصویر صفحه هوم"
        verbose_name_plural = "تصاویر صفحه هوم"


class Consult (models.Model ) : 
    
    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    first_name = models.CharField(max_length=256,verbose_name="نام")

    last_name = models.CharField(max_length=256,verbose_name="نام خانوادگی")

    phone = models.SlugField(max_length=11,verbose_name="شماره همراه")

    email = models.EmailField(verbose_name="ایمیل")

    text = models.TextField(verbose_name="توضیحات")

    is_valid = models.BooleanField(default=False,verbose_name="تایید شده توسط ادمین")

    def __str__(self) : 
        return  f"{self.first_name} {self.last_name}"
    
    class Meta : 
        verbose_name = "درخواست مشاوره "
        verbose_name_plural = 'درخواست های مشاوره کاربران'
    
    def clean(self) : 
        if not regex_phone.findall(self.phone) : 
            raise ValidationError("phone must be integer and 11 character .")

# گواهینامه ها
class License (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    title = models.CharField(max_length=256,verbose_name="عنوان")

    icon = models.ImageField(upload_to="home/license/icon/",verbose_name="آیکون گواهینامه")

    description = models.TextField(verbose_name="توضیحات گواهینامه")

    def __str__(self) : 
        return str(self.title)
    
    class Meta : 
        verbose_name = "گواهی نامه"
        verbose_name_plural = "گواهی نامه ها"