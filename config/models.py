from django.db import models
from uuid import uuid4
from utils.models import Item

# مدل کلی تنظیمات
class Settings(models.Model) : 

    logo = models.ImageField(upload_to="settings/logo",verbose_name="لوگو",null=True,blank=True)

    description = models.TextField(null=True,blank=True,verbose_name="توضیحات قسمت فوتر")

    address = models.TextField(null=True,blank=True,verbose_name="آدرس")

    class Meta : 
        verbose_name = "تنظیمات"
        verbose_name_plural = "تنظیمات"
    
    def __str__(self) : 
        return "تنظیمات"

# مدل داستان ما
class Story(models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    settings = models.OneToOneField(Settings,on_delete=models.CASCADE,related_name="story",default=1)

    text = models.TextField(verbose_name="داستان ما")

    class Meta : 
        verbose_name = "داستان"
        verbose_name_plural = "داستان ما"
    
    def __str__(self) : 
        return str(self.text)

# مدل دستاورد ها 
class Achievements(models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    settings = models.OneToOneField(Settings,on_delete=models.CASCADE,default=1,related_name="achievements")

    customer_count = models.PositiveIntegerField(verbose_name="تعداد مشتری ها ")

    building = models.PositiveIntegerField(verbose_name="در حال ساخت")

    checking = models.PositiveIntegerField(verbose_name="در حال بررسی")

    complete = models.PositiveIntegerField(verbose_name="پروژه های تکمیلی")

    def __str__(self) : 
        return "دستاورد ها"
    
    class Meta : 
        verbose_name = "دستاورد"
        verbose_name_plural = "دستاورد های ما"


# نحوه ثبت سفارش
class OrderingGuide(Item) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    settings = models.ForeignKey(Settings,on_delete=models.CASCADE,related_name="ordering_guide",default=1)

    class Meta : 
        verbose_name = "نحوه ثبت سفارش"
        verbose_name_plural = "راهنمای سفارش"



# سوالات متداول
class Feq(Item) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    settings = models.ForeignKey(Settings,on_delete=models.CASCADE,related_name="feqs",default=1)

    class Meta : 
        verbose_name = "سوال "
        verbose_name_plural = "سوالات متداول"

# راه های ارتباطی
class ContactItem(Item) : 

    settings = models.ForeignKey(
        Settings,
        on_delete=models.CASCADE,
        related_name="contact_items",
        default=1)
    
    class Meta : 
        verbose_name = "راه ارتباطی"
        verbose_name_plural = "راه های ارتباطی"


# شبکه های اجتماعی
class SocialContact(models.Model) : 

    settings = models.ForeignKey(
        Settings,
        on_delete=models.CASCADE,
        related_name="socials",
        default=1
    )

    icon = models.ImageField(upload_to="config/socials/",verbose_name="آیکون")

    url = models.URLField(verbose_name="آدرس")

    def __str__(self) : 
        return "social contact"
    
    class Meta : 
        verbose_name = "شبکه اجتماعی"
        verbose_name_plural = "شبکه های اجتماعی"