from django.db import models
from django.contrib.auth import get_user_model
from product.models import Count
from django_jalali.db.models import jDateTimeField
from uuid import uuid4
from django_jalali.db.models import jDateTimeField
from django.core.exceptions import ValidationError
import re
from random import randint
from driver.models import Driver

number_regex = re.compile("^[0-9]{8,}$")


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

    products_count = models.ManyToManyField(
        to = Count,
        blank=True,
        verbose_name="محصولات"
    )

    is_send =models.BooleanField(default=False,verbose_name="ارسال شده")

    is_valid = models.BooleanField(default=False,verbose_name="تایید شده")

    created  = jDateTimeField(auto_now_add=True)

    tracking_code = models.SlugField(null=True,blank=True,verbose_name="کد رهگیری")

    driver = models.ForeignKey(
        to = Driver , 
        on_delete = models.SET_NULL ,
        null = True , 
        blank = True ,
        verbose_name = "راننده" 
    )

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
    
    def save(self,**kwargs) : 
        if not self.tracking_code : 
            self.tracking_code = f"ksp_{randint(10000,99999)}"
        return super().save(**kwargs)



# مدل قوانین 
class Rule (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    text = models.TextField(verbose_name="متن")

    def __str__ (self) : 
        return "قانون"
    
    class Meta : 
        verbose_name ="قانون"
        verbose_name_plural = 'قوانین و مقررات'


# مدل فیش واریزی

class PaySlip (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    order = models.ForeignKey(
        to = Order,
        on_delete = models.CASCADE,
        related_name = "pay_slips"
    )

    name = models.CharField(max_length=256,verbose_name="نام و نام خانوادگی واریز کننده")

    credit_card_number = models.SlugField(verbose_name="شماره حساب")

    image = models.ImageField(
        upload_to="order/slip/",
        verbose_name="تصویر فیش واریزی"
    )

    iban = models.SlugField(verbose_name="شماره شبا")

    time = jDateTimeField(verbose_name="تاریخ واریز") 

    order_tracking_number = models.IntegerField(verbose_name="شماره پیگیری سفارش", null=True)

    sheba_number = models.PositiveBigIntegerField(verbose_name="شماره کارت واریز کننده", null=True)

    description = models.TextField(verbose_name="توضیحات", null=True)

    def __str__ (self) : 
        return str(self.name)
    
    class Meta : 
        verbose_name = "فیش واریزی"
        verbose_name_plural = "فیش های واریزی"

    def clean(self) : 
        if not number_regex.findall(self.iban) : 
            raise ValidationError("iban must be number and at least 8 character .")
        
        if not number_regex.findall(self.credit_card_number) : 
            raise  ValidationError("creadit card number must be number and at least 8 character .")