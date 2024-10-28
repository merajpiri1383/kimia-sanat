from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model
from random import randint
from django_jalali.db.models import jDateTimeField

# مدل تیکت

ticket_status = [
    ("closed","بسته شده"),
    ("responsed","پاسخ داده شد"),
    ("pending-admin","در انتظار پاسخ ادمین"),
    ("pending","در انتظار بررسی"),
    ("responsed-user","پاسخ توسط مشتری")
]

class Ticket (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    user = models.ForeignKey(
        to = get_user_model() , 
        verbose_name = "کاربر" , 
        on_delete = models.CASCADE ,
        related_name="tickets"
    )

    title = models.CharField(max_length=256,verbose_name="عنوان",null=True,blank=True)

    is_from_admin = models.BooleanField(default=False,verbose_name="از طرف ادمین است ")

    reply_to = models.ForeignKey(
        to = "Ticket",
        on_delete = models.CASCADE , 
        related_name = "replys",
        null=True,
        blank=True
    )

    text = models.TextField(verbose_name="توضیحات")

    created = jDateTimeField(auto_now_add=True,verbose_name="تاریخ")

    number = models.SlugField(null=True,blank=True,verbose_name="شماره تیکت")

    status = models.CharField(verbose_name="وضعیت",choices=ticket_status,default="pending")

    def __str__ (self) : 
        return str(self.user)
    
    class Meta : 
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"

    def save(self,**kwargs) : 
        if not self.number : 
            self.number = f"ksp{randint(10000,99999)}"
        if self.is_from_admin : 
            self.status = "closed"
        return super().save(**kwargs)


# فایل های تیکت

class TicketFile (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    ticket = models.ForeignKey(
        to = Ticket , 
        on_delete = models.CASCADE , 
        related_name = "files",
    )

    file = models.FileField(upload_to="ticket/files/",verbose_name="فایل")

    def __str__(self) : 
        return str(self.file)
    
    class Meta : 
        verbose_name = "فایل"
        verbose_name_plural = "فایل ها"


# مدل بازخورد کامنت 


types_feedback = [
    ('good','خوب'),
    ('middle','متوسط'),
    ('bad','بد')
]

class Feedback ( models.Model ) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True) 

    user = models.ForeignKey(
        to = get_user_model(),
        on_delete = models.CASCADE,
        related_name="feedbacks",
        verbose_name = "کاربر"
    )

    ticket = models.OneToOneField(
        to = Ticket , 
        on_delete = models.CASCADE , 
        related_name = "feedback",
        verbose_name="تیکت",
        null=True,
        blank=True
    ) 

    type = models.CharField(verbose_name="نوع بازخورد",max_length=10,choices=types_feedback,default="middle")

    description = models.TextField(verbose_name="توضیحات",null=True,blank=True)

    def __str__ (self) : 
        return str(self.type)
    
    class Meta : 
        verbose_name = 'بازخورد'
        verbose_name_plural = 'بازخورد تیکت'


# صفحه تیکت ها 

class TicketPage (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    title = models.CharField(max_length=256,verbose_name="عنوان کادر",null=True,blank=True)

    text = models.TextField(verbose_name="متن کادر",null=True,blank=True)

    def __str__ (self) : 
        return "صفحه تیکت ها"
    
    class Meta : 
        verbose_name = "صفحه تیکت ها"
        verbose_name_plural = "صفحه تیکت ها"