from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model
from django_jalali.db.models import jDateTimeField

# مدل تیکت

ticket_status = [
    ("closed","بسته شده"),
    ("responsed","پاسخ داده شد"),
    ("pending-admin","در انتظار پاسخ ادمین"),
    ("checking","در انتظار بررسی"),
    ("pending-user","در انتظار پاسخ کاربر")
]

class Ticket (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    user = models.ForeignKey(
        to = get_user_model() , 
        verbose_name = "کاربر" , 
        on_delete = models.CASCADE ,
        related_name="tickets"
    )

    title = models.CharField(max_length=256,verbose_name="عنوان")

    department = models.CharField(max_length=256,verbose_name="دپارتمان")

    reply_to = models.ForeignKey(
        to = "Ticket",
        on_delete = models.CASCADE , 
        related_name = "replys",
        null=True,
        blank=True
    )

    text = models.TextField(verbose_name="توضیحات")

    created = jDateTimeField(auto_now_add=True,verbose_name="تاریخ")

    status = models.CharField(verbose_name="وضعیت",choices=ticket_status,default="closed")

    def __str__ (self) : 
        return str(self.user)
    
    class Meta : 
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"


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