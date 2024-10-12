from django.db import models
from uuid import uuid4
from django_jalali.db.models import jDateTimeField
from django.core.exceptions import ValidationError
import re

class Item(models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    key = models.CharField(max_length=256,verbose_name="کلید")

    value = models.CharField(max_length=256,verbose_name="مقدار")

    class Meta : 
        abstract = True

    def __str__(self) : 
        return str(self.key)


# مدل پایه کامنت

phone_regex = re.compile("^0[0-9]{10}$")

class CommentBase (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    name = models.CharField(max_length=256,verbose_name='نام و نام خانوادگی')

    phone = models.SlugField(verbose_name="شماره تلفن")

    email = models.EmailField(verbose_name="ایمیل",null=True,blank=True)

    reply_to = models.ForeignKey(
        to = "Comment",
        on_delete = models.CASCADE,
        related_name = "replys",
        null=True,
        blank=True
    )

    description = models.TextField(verbose_name="پیام کاربر")

    is_valid = models.BooleanField(default=False,verbose_name="تایید شده توسط ادمین")

    created = jDateTimeField(auto_now_add=True,verbose_name="زمان ایجاد")

    def __str__(self) : 
        return str(self.name)
    
    class Meta : 
        abstract = True

    def clean(self) : 
        if not phone_regex.findall(self.phone) : 
            raise ValidationError("invalid phone number .")