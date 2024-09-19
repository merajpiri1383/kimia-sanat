from django.db import models
from django.contrib.auth import get_user_model
from product.models import Count
from django_jalali.db.models import jDateTimeField
from uuid import uuid4


delivery_times = [
    ("12","12 ساعت"),
    ("24","24 ساعت"),
    ("72","72 ساعت")
]

delivery_type = (
    ("driver","معرفی راننده"),
    ("send-factory","ارسال از درب کارخانه"),
    ("factory","تحویل درب کارخانه")
)

# سفارش
class Order (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    user = models.ForeignKey(
        to = get_user_model(),
        on_delete = models.CASCADE,
        related_name = "orders"
    )

    products = models.ManyToManyField(
        to = Count,
        blank=True,
        verbose_name="محصولات"
    )

    is_paid =models.BooleanField(default=False,verbose_name="پرداخت شده")

    is_valid = models.BooleanField(default=False,verbose_name="تایید شده")

    created  = jDateTimeField(auto_now_add=True)

    delivery_time = models.CharField(
        max_length=2,
        verbose_name="زمان تحویل کالا",
        choices=delivery_times,
        default="24"
        )
    
    delivery_type = models.CharField(
        max_length=20,
        choices=delivery_type,
        default="send-factory",
        verbose_name="نوع تحویل"
    )

    ident_code = models.SlugField(max_length=5,verbose_name="کد معرف",null=True,blank=True)

    def __str__ (self) : 
        return f"cart - {self.user.phone}"
    
    class Meta : 
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'