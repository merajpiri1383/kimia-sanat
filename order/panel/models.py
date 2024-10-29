from django.db import models
from uuid import uuid4


# صفحه لیست خرید های من 

class ListShopPage (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    title = models.CharField(
        max_length=256,
        verbose_name="عنوان کادر",
        null=True,
        blank=True,
    )

    text = models.TextField(
        verbose_name="متن",
        null=True,
        blank=True
    )

    def __str__ (self) : 
        return "صفحه لیست خرید های من"
    
    class Meta : 
        verbose_name = "صفحه لیست خرید های من"
        verbose_name_plural = "صفحه لیست خرید های من"



# صفحه لیست محصولات / سفارش محصول 

class OrderPage (models.Model) : 

    id = models.UUIDField(
        default=uuid4,
        unique=True,
        primary_key=True,
    )

    title = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name="عنوان کادر ",
    )

    text = models.TextField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name="متن کادر"
    )

    def __str__(self) : 
        return "صفحه سفارش "
    
    class Meta : 
        verbose_name = "صفحه سفارش"
        verbose_name_plural = "صفحه سفارش"


class MyOrderPage (models.Model) : 

    id = models.UUIDField(
        default=uuid4,
        unique=True,
        primary_key=True,
    )

    title = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name="عنوان",
    )

    text = models.TextField(
        null=True,
        blank=True,
        verbose_name="متن",
    )

    def __str__ (self) : 
        return "صفحه سوابق خرید"
    
    class Meta : 
        verbose_name = "سوابق خرید"
        verbose_name_plural = "صفحه سوابق خرید"
