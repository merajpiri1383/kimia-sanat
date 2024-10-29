from django.db import models
from uuid import uuid4

class Header (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    logo = models.ImageField(upload_to="header/logo/",verbose_name="لوگو سایت",null=True,blank=True)

    phone = models.SlugField(verbose_name="شماره تلفن داخل هدر",null=True,blank=True)

    email = models.EmailField(verbose_name="ایمیل داخل هدر",null=True,blank=True)


    def __str__(self) : 
        return "هدر"
    
    class Meta : 
        verbose_name ="هدر"
        verbose_name_plural = "مدیرت هدر"

# مدل منو 
class Menu (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    header = models.ForeignKey(Header,on_delete=models.CASCADE,related_name="menus")

    name = models.CharField(max_length=256,verbose_name="نام منو")

    internal_url = models.CharField(max_length=256,null=True,blank=True,verbose_name="لینک داخلی")

    external_url = models.URLField(null=True,blank=True,verbose_name="لینک خارجی")

    def __str__(self) : 
        return str(self.name)
    
    class Meta : 
        verbose_name = "منو"
        verbose_name_plural = 'مدیرت منو  هدر'


# زیر منو 
class SubMenu (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    menu = models.ForeignKey(
        to = Menu,
        on_delete=models.CASCADE,
        related_name="sub_menus",
    )

    name = models.CharField(max_length=256,verbose_name="زیر منو")

    interal_url = models.CharField(max_length=256,null=True,blank=True,verbose_name="لینک داخلی ")

    external_url = models.URLField(null=True,blank=True,verbose_name="لینک خارجی")

    def __str__(self) : 
        return str(self.name)
    
    class Meta : 
        verbose_name = "زیر منو"
        verbose_name_plural = "زیر منو ها"