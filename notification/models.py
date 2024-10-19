from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model
from django_jalali.db.models import jDateTimeField

class NotificationPage ( models.Model ) : 
    
    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    card_title = models.CharField(
        max_length=256,
        verbose_name="عنوان کادر",
        null=True,
        blank=True
        )
    
    card_description = models.TextField(
        null=True,
        blank=True,
        verbose_name="توضیحات کادر"
    )

    def __str__(self) : 
        return "صفحه اعلانات"

    class Meta : 
        verbose_name = "صفحه اعلانات"
        verbose_name_plural = "مدیرت صفحه اعلانات"



# اعلان

class Notification (models.Model) :
    
    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="کاربر",
        null=True,
        blank=True
    )

    send_to_all = models.BooleanField(default=False,verbose_name="ارسال به همه")

    title = models.CharField(max_length=256,verbose_name="عنوان اعلان")

    text = models.TextField(verbose_name="متن اعلان")

    read_users = models.ManyToManyField(
        to=get_user_model(),
        blank=True,
        related_name="readers"
    )

    created = jDateTimeField(auto_now_add=True,verbose_name="تاریخ ارسال")

    class Meta : 
        verbose_name = "اعلان"
        verbose_name_plural = "اعلانات"

    def __str__ (self) : 
        return str(self.title)
    
