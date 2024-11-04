from django.db import models
from uuid import uuid4

# گروه محصول

class GroupProduct (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    name = models.CharField(max_length=256,unique=True,verbose_name="نام گروه")

    def __str__(self) : 
        return str(self.name)
    
    class Meta : 
        verbose_name = "گروه محصولات"
        verbose_name_plural = "گروه های محصولات"


# محصول
class ProductSystem (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    group = models.ForeignKey(
        to = GroupProduct ,
        on_delete = models.CASCADE , 
        related_name = "products",
        verbose_name="گروه"
    )

    product_code = models.SlugField(verbose_name="کد محصول",unique=True,blank=True)

    name = models.CharField(max_length=256,verbose_name="نام محصول")

    colleague_price = models.PositiveBigIntegerField(
        null=True,
        blank=True
        ,verbose_name="قیمت هر کیلو گرم برای همکار(ریال)"
    )
    
    buy_price = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name="قیمت هر کیلو گرم برای فروش (ریال)"
    )

    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    

    def __str__(self) : 
        return str(self.name)
    
    class Meta : 
        verbose_name = "محصول"
        verbose_name_plural = "محصولات سیستم"
        ordering = ["created"]