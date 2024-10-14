from typing import Iterable
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
from system.models import ProductSystem

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

    official_invoice = models.FileField(
        upload_to = "order/official-invoice/",
        verbose_name = "فاکتور رسمی",
        null = True , 
        blank = True
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
        return "قوانین و مقررات خرید کاربر"
    
    class Meta : 
        verbose_name = "قوانین و مقررات خرید کاربر"
        verbose_name_plural = "قوانین و مقررات خرید کاربر"


# مدل فیش واریزی

class PaySlip (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    order = models.ForeignKey(
        to = Order,
        on_delete = models.CASCADE,
        related_name = "pay_slips"
    )

    name = models.CharField(max_length=256,verbose_name="نام و نام خانوادگی واریز کننده")

    image = models.ImageField(
        upload_to="order/slip/",
        verbose_name="تصویر فیش واریزی"
    )

    time = jDateTimeField(verbose_name="تاریخ واریز") 

    order_tracking_number = models.IntegerField(verbose_name="شماره پیگیری سفارش", null=True)

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
        


# پیش فاکتور 

class PreInvoice (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    order = models.OneToOneField(
        to = Order ,
        on_delete = models.CASCADE , 
        related_name = "pre_invoice",
    )

    total_price = models.PositiveBigIntegerField(default=0,verbose_name="قیمت نهایی",null=True,blank=True)

    is_for_collegue = models.BooleanField(default=False,verbose_name="برای همکار است")

    is_for_customer = models.BooleanField(default=False,verbose_name="برای مشتری است")

    is_final = models.BooleanField(default=False,verbose_name="نهایی شده")

    def save(self,**kwargs) : 
        total = 0
        for product in self.products.all() : 
            total = total + product.total_price
        self.total_price = total
        return super().save(**kwargs)

    class Meta : 
        verbose_name = "پیش فاکتور"
        verbose_name_plural = "پیش فاکتور ها"

    def __str__ (self) : 
        return "پیش فاکتور"
    

class PreInvoiceProduct (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    title = models.ForeignKey(
        to = ProductSystem , 
        on_delete = models.CASCADE , 
        verbose_name = "شرح کالا"
    )

    pre_invoice = models.ForeignKey(
        to = PreInvoice , 
        on_delete = models.CASCADE,
        related_name = "products",
    )

    count = models.PositiveBigIntegerField(default=1,verbose_name="مقدار")

    unit = models.CharField(max_length=256,verbose_name="واحد",default="کیلو گرم")

    colleague_price = models.PositiveBigIntegerField(
        null=True,
        blank=True
        ,verbose_name="قیمت برای همکار"
    )
    
    buy_price = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name="قیمت برای فروش"
    )

    total_price = models.PositiveBigIntegerField(default=0,verbose_name="مجموع")


    def clean(self) -> None:
        self.colleague_price = self.title.colleague_price
        self.buy_price = self.title.buy_price
        if self.pre_invoice.is_for_collegue : 
            self.total_price = self.count * self.title.colleague_price
        elif self.pre_invoice.is_for_customer : 
            self.total_price = self.count * self.title.buy_price
        self.save()
        self.pre_invoice.save()
        return super().clean()

    def __str__ (self) : 
        return str(self.title)
    
    class Meta : 
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"