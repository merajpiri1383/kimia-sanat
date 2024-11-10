from django.db import models
from uuid import uuid4
import re
from django.core.exceptions import ValidationError

regex_phone = re.compile("^0[0-9]{10}$")


class Footer (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    logo = models.ImageField(upload_to="template/footer/logo/",verbose_name="لوگو ",null=True,blank=True)

    logo_title = models.CharField(max_length=256,verbose_name="عنوان لوگو",null=True,blank=True)

    logo_sub_title = models.CharField(max_length=256,verbose_name="زیر عنوان لوگو",null=True,blank=True)

    text = models.TextField(null=True,blank=True,verbose_name="متن فوتر")

    link_footer_title = models.CharField(max_length=256,verbose_name="عنوان ستون لینک ها",null=True,blank=True)

    category_footer_title = models.CharField(max_length=128,null=True,blank=True,verbose_name="عنوان ستون لینک ها ۲")

    copyright_text = models.TextField(verbose_name="متن کپی رایت",null=True,blank=True)

    inamad_code = models.TextField(null=True,blank=True,verbose_name="کد اینماد")

    instagram_link = models.URLField(verbose_name="آدرس اینستاگرام",null=True,blank=True)

    linkedin_link = models.URLField(verbose_name="آدرس لینکدین",null=True,blank=True)

    telegram_link = models.URLField(verbose_name="آدرس تلگرام",null=True,blank=True)

    eitaa_link = models.URLField(verbose_name="آدرس ایتا",null=True,blank=True)

    soroush_link = models.URLField(verbose_name="آدرس سروش",null=True,blank=True)

    def __str__ (self) : 
        return "فوتر"
    
    class Meta : 
        verbose_name = "فوتر"
        verbose_name_plural = "فوتر"


class PhoneFooter (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    footer = models.ForeignKey(Footer,on_delete=models.CASCADE,related_name="phones")

    phone = models.CharField(max_length=256,verbose_name="شماره")

    is_constant = models.BooleanField(default=False,verbose_name="شماره ثابت است")

    is_fax = models.BooleanField(default=False,verbose_name="شماره فکس است")

    def __str__ (self) : 
        return str(self.phone)
    
    class Meta : 
        verbose_name = "شماره تلفن فوتر"
        verbose_name_plural = "شماره های فوتر"

class ElectroLicense (models.Model) : 

    id = models.UUIDField(unique=True,primary_key=True,default=uuid4)

    footer = models.ForeignKey(
        to = Footer,
        on_delete=models.CASCADE,
        related_name="licenses"
    )

    image = models.ImageField(upload_to="template/footer/image/",verbose_name="تصویر")

    url = models.URLField(verbose_name="آدرس",null=True,blank=True)

    class Meta : 
        verbose_name = "مجوز فوتر "
        verbose_name_plural = "مجوز های فوتر"

    def __str__(self) : 
        return "مجوز "
    
class FooterLink (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    footer = models.ForeignKey(Footer,on_delete=models.CASCADE,related_name="links")

    name = models.CharField(max_length=256,verbose_name="نام لینک")

    internal_url = models.URLField(verbose_name="ادرس داخلی",null=True,blank=True)

    external_url = models.URLField(verbose_name="ادرس خارجی",null=True,blank=True)

    def __str__ (self) : 
        return str(self.name)
    
    class Meta : 
        verbose_name = "لینک فوتر"
        verbose_name_plural = "لینک های فوتر ستون ۱"

class CategoryFooter (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    footer = models.ForeignKey(Footer,on_delete=models.CASCADE,related_name="categories")

    name = models.CharField(max_length=256,verbose_name="نام لینک")

    url = models.URLField(verbose_name="آدرس")

    def __str__(self) : 
        return str (self.name)
    
    class Meta : 
        verbose_name = "لینک فوتر"
        verbose_name_plural = "لینک های فوتر ستون ۲"



# مدل باشگاه مشتریان 
class CustomerClub (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    phone = models.SlugField(verbose_name="شماره",unique=True)

    def __str__ (self) : 
        return str(self.phone)
    
    class Meta : 
        verbose_name = "مشتری"
        verbose_name_plural = "باشگاه مشتریان"
    
    def clean(self) : 

        if not regex_phone.findall(self.phone) : 
            raise ValidationError("invalid phone number .")
        

# سوالات متداول فوتر 

class FooterFeq (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    footer = models.ForeignKey(
        to = Footer , 
        on_delete = models.CASCADE , 
        related_name = "feqs"
    )

    question = models.CharField(verbose_name="سوال",max_length=256)

    answer = models.TextField(verbose_name="پاسخ")

    created = models.DateTimeField(null=True,blank=True,auto_now_add=True)

    def __str__ (self) : 
        return str (self.question)
    
    class Meta : 
        verbose_name = "سوال فوتر"
        verbose_name_plural = "سوالات متداول فوتر"
        ordering = ["created"]