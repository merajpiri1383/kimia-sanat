from django.db import models
from uuid import uuid4
from utils.models import Item


# صفحه تماس با ما
class ContactUs (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    instagram_link = models.URLField(verbose_name="آدرس اینستاگرام",null=True,blank=True)

    linkedin_link = models.URLField(verbose_name="آدرس لینکدین",null=True,blank=True)

    telegram_link = models.URLField(verbose_name="آدرس تلگرام",null=True,blank=True)

    eitaa_link = models.URLField(verbose_name="آدرس ایتا",null=True,blank=True)

    soroush_link = models.URLField(verbose_name="آدرس سروش",null=True,blank=True)

    def __str__ (self) : 
        return "صفحه تماس با ما"

    class Meta : 
        verbose_name = "صفحه تماس با ما"
        verbose_name_plural = "مدیرت صفحه تماس با ما"

class ContactTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    contact = models.OneToOneField(ContactUs,on_delete=models.CASCADE,related_name="contact_title")

    title = models.CharField(max_length=256,null=True,blank=True,verbose_name="عنوان بالایی تماس با ما")

    sub_title = models.CharField(max_length=256,null=True,blank=True,verbose_name="عنوان پایینی تماس با ما")

    address = models.TextField(null=True,blank=True,verbose_name="آدرس")

    side_image = models.ImageField(upload_to="config/contact-us/side-image/",verbose_name="تصویر کناری",null=True,blank=True)

    def __str__(self) : 
        return "عنوان کادر تماس با ما"
    
    class Meta : 
        verbose_name = "عنوان کادر تماس با ما"
        verbose_name_plural = "عنوان کادر تماس با ما"

# راه های ارتباطی
class ContactItem(Item) : 
    
    contact = models.ForeignKey(ContactUs,on_delete=models.CASCADE,related_name="contact_items")

    class Meta : 
        verbose_name = "راه ارتباطی"
        verbose_name_plural = "راه های ارتباطی"


# عنوان شبکه اجتماعی
class SocialTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    contact = models.OneToOneField(ContactUs,on_delete=models.CASCADE,related_name="social_title")

    title = models.CharField(max_length=256,null=True,blank=True,verbose_name="عنوان بالایی شبکه های اجتماعی")

    sub_title = models.CharField(max_length=256,null=True,blank=True,verbose_name="عنوان پاینی شبکه های اجتماعی")

    def __str__(self) : 
        return "عنوان شبکه های اجتماعی"
    
    class  Meta : 
        verbose_name = "عنوان شبکه های اجتماعی"
        verbose_name_plural = "مدیرت عنوان شبکه های اجتماعی"



# مدل نقشه 
class Location (models.Model) : 

    id = models.UUIDField(unique=True,primary_key=True,default=uuid4)

    contact = models.OneToOneField(ContactUs,on_delete=models.CASCADE,related_name="location") 

    title = models.CharField(max_length=256,verbose_name="عنوان کادر نقشه",null=True,blank=True)

    sub_title = models.CharField(max_length=256,verbose_name="زیر عنوان کادر نقشه",null=True,blank=True)

    location_latitude = models.DecimalField(null=True,
                                            blank=True,
                                            max_digits=12,
                                            decimal_places=8,
                                            verbose_name="عرض جغرافیایی")

    location_longitude = models.DecimalField(
                                            null=True,
                                            blank=True, 
                                            verbose_name="طول جغرافیایی",
                                            max_digits=12,
                                            decimal_places=8
                                            )

    def __str__ (self) : 
        return "نقشه"
    
    class Meta : 
        verbose_name = "نقشه"
        verbose_name_plural = "مدیرت موقیعت مکانی"