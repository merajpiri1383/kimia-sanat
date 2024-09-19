from django.db import models
from uuid import uuid4
from django_jalali.db.models import jDateTimeField
import re
from django.core.exceptions import ValidationError

phone_regex = re.compile("0[0-9]{10}")


# مدل راننده 
class Driver (models.Model) : 
    
    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    name = models.CharField(max_length=256,verbose_name="نام راننده",unique=True)

    license_plate = models.SlugField(max_length=8,verbose_name="پلاک راننده",unique=True)

    car = models.CharField(max_length=256,verbose_name="ماشین راننده")

    phone = models.SlugField(max_length=11,verbose_name="شماره راننده",unique=True)

    national_id = models.PositiveBigIntegerField(verbose_name="کد ملی",unique=True)

    created = jDateTimeField(auto_now_add=True)

    def __str__ (self) : 
        return str (self.name)
    
    class Meta : 
        verbose_name = "راننده"
        verbose_name_plural = "راننده ها"

    def clean(self) : 
        if not phone_regex.findall(self.phone) : 
            raise ValidationError("please enter correct phone number .")