from django.db import models
from uuid import uuid4
from django_jalali.db.models import jDateTimeField
import re
from django.core.exceptions import ValidationError

phone_regex = re.compile("0[0-9]{10}")


# مدل راننده 
class Driver (models.Model) : 
    
    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    name = models.CharField(max_length=256,verbose_name="نام راننده")

    license_plate = models.CharField(max_length=12,verbose_name="پلاک راننده")

    car = models.CharField(max_length=256,verbose_name="ماشین راننده")

    phone = models.SlugField(max_length=11,verbose_name="شماره راننده")

    national_id = models.PositiveBigIntegerField(verbose_name="شناسه راننده")

    created = jDateTimeField(auto_now_add=True)

    def __str__ (self) : 
        return str (self.name)
    
    class Meta : 
        verbose_name = "راننده"
        verbose_name_plural = "راننده ها"

    def clean(self) : 
        if not phone_regex.findall(self.phone) : 
            raise ValidationError("please enter correct phone number .")
        

# صفحه لیست راننده ها 

class DriverListPage (models.Model) : 

    id = models.UUIDField(
        default=uuid4,
        unique=True,
        primary_key=True,
    )

    title = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name="عنوان کادر"
    )

    text = models.TextField(
        verbose_name="متن",
        null=True,
        blank=True
    )

    def __str__ (self) : 
        return "صفحه لیست راننده ها"
    
    class Meta : 
        verbose_name = "صفحه لیست راننده ها"
        verbose_name_plural = "صفحه لیست راننده ها"


class DriverAddPage (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    title = models.CharField(max_length=256,verbose_name="عنوان ",null=True,blank=True)

    text = models.TextField(null=True,blank=True,verbose_name="متن")

    def __str__ (self) : 
        return "صفحه افزودن راننده"
    
    class Meta : 
        verbose_name = "صفحه افزودن راننده"
        verbose_name_plural = "صفحه افزودن راننده"