from django.db import models
from uuid import uuid4
from django_jalali.db.models import jDateTimeField

class Item(models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    key = models.CharField(max_length=256,verbose_name="کلید")

    value = models.TextField(verbose_name="مقدار")

    class Meta : 
        abstract = True

    def __str__(self) : 
        return str(self.key)


# مدل پایه کامنت
class CommentBase (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    name = models.CharField(max_length=256,verbose_name='نام و نام خانوادگی')

    email = models.EmailField(verbose_name="ایمیل",null=True,blank=True)

    reply_to = models.ForeignKey(
        to = "Comment",
        on_delete = models.CASCADE,
        related_name = "replys",
        verbose_name="پاسخ به",
        null=True,
        blank=True
    )

    description = models.TextField(verbose_name="توضیحات")

    is_valid = models.BooleanField(default=False,verbose_name="تایید شده توسط ادمین")

    created = jDateTimeField(auto_now_add=True,verbose_name="زمان ایجاد")

    def __str__(self) : 
        return str(self.name)
    
    class Meta : 
        abstract = True