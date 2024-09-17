from django.db import models
from django.core.exceptions import ValidationError
from uuid import uuid4
import re


regex_phone = re.compile("^0[0-9]{10}$")


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