from django.db import models
from uuid import uuid4


# صفحه کارت های شرکت

class CompanyCardsPage (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    title = models.CharField(max_length=256,verbose_name="عنوان کادر",null=True,blank=True)

    text = models.TextField(verbose_name="متن کادر",null=True,blank=True)
    

    def __str__ (self) : 
        return "صفحه شماره کارت های شرکت"
    
    class Meta : 
        verbose_name = "صفحه شماره کارت های شرکت"
        verbose_name_plural = "صفحه شماره کارت های شرکت"


# شماره کارت های شرکت

class CompanyCard (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    page = models.ForeignKey(
        to = CompanyCardsPage , 
        on_delete = models.CASCADE , 
        related_name = "cards"
    )

    bank_name = models.CharField(max_length=256,verbose_name="نام بانک")

    bank_icon = models.ImageField(
        upload_to="template/company-page/",
        null=True,
        blank=True,
        verbose_name="آیکون بانک"
    )

    card_number = models.SlugField(verbose_name="شماره کارت")

    sheba_number = models.SlugField(verbose_name="شماره شبا")

    def __str__ (self) : 
        return str(self.bank_name)
    
    class Meta : 
        verbose_name = "شماره کارت"
        verbose_name_plural = "شماره کارت های شرکت"


# صفحه ذخیره شده ها 

class SavedPage (models.Model) : 
    
    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    title = models.CharField(max_length=256,verbose_name="عنوان کادر")

    text = models.TextField(verbose_name="متن کادر")

    def __str__ (self) : 
        return  "صفحه ذخیره شده ها"
    
    class Meta : 
        verbose_name = "صفحه ذخیره شده ها"
        verbose_name_plural =  "صفحه ذخیره شده ها"
