from django.db import models
from uuid import uuid4
from utils.models import Item
from project.models import Project
    
# صفحه درباره ما 
class AboutUs (models.Model) : 

    background_title = models.CharField(max_length=256,verbose_name="عنوان روی بک گراند",null=True,blank=True)
    
    background = models.ImageField(upload_to="config/about/background/",verbose_name="بکگراند صفحه درباره ما",null=True,blank=True)

    projects = models.ManyToManyField(
        to = Project,
        blank=True,
        verbose_name="پروژه های صفحه درباره ما"
    )

    def __str__ (self) : 
        return "صفحه درباره ما"
    
    class Meta : 
        verbose_name = "صفحه درباره ما"
        verbose_name_plural = "مدیرت صفحه درباره ما"


# مدل داستان ما
class Story(models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    about = models.OneToOneField(AboutUs,on_delete=models.CASCADE,related_name="story")

    title = models.CharField(max_length=256,verbose_name='عنوان بالا',null=True,blank=True)

    sub_title = models.CharField(max_length=256,verbose_name="عنوان پایینی",null=True,blank=True)   

    side_image = models.ImageField(upload_to="about/story/side-image/",verbose_name="تصویر کناری",null=True,blank=True)

    text = models.TextField(verbose_name="داستان ما")

    class Meta : 
        verbose_name = "داستان"
        verbose_name_plural = "داستان ما"
    
    def __str__(self) : 
        return str(self.text)
    
class StoryItem (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    story = models.ForeignKey(
        to = Story,
        on_delete = models.CASCADE,
        related_name = "items",
    )

    value = models.CharField(max_length=256,verbose_name="مقدار")

    def __str__ (self) : 
        return str (self.value)
    
    class Meta : 
        verbose_name = "آیتم داستان"
        verbose_name_plural = "آیتم های داستان"


# مدل دستاورد ها 
class Achievements(models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    about = models.OneToOneField(AboutUs,on_delete=models.CASCADE,related_name="achievements")

    title = models.CharField(max_length=256,null=True,blank=True,verbose_name="عنوان دستاورد ها ")

    sub_title = models.CharField(max_length=256,null=True,blank=True,verbose_name="عنوان پایینی")

    icon = models.ImageField(upload_to="config/about/ordering/icon/",verbose_name="ایکون",null=True,blank=True)

    customer_count = models.PositiveIntegerField(verbose_name="تعداد مشتری ها ")

    building = models.PositiveIntegerField(verbose_name="در حال ساخت")

    checking = models.PositiveIntegerField(verbose_name="در حال بررسی")

    complete = models.PositiveIntegerField(verbose_name="پروژه های تکمیلی")

    def __str__(self) : 
        return "دستاورد ها"
    
    class Meta : 
        verbose_name = "دستاورد"
        verbose_name_plural = "دستاورد های ما"

# عنوان ثبت سفارش
class OrderGuideTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    about = models.OneToOneField(AboutUs,on_delete=models.CASCADE,related_name="order_guide_title")

    title = models.CharField(max_length=256,null=True,blank=True,verbose_name="عنوان ثبت سفارش")

    sub_title = models.CharField(max_length=256,null=True,blank=True,verbose_name="عنوان پایینی")

    icon = models.ImageField(upload_to="config/about/ordering/icon/",verbose_name="ایکون",null=True,blank=True)

    def __str__(self) : 
        return "عنوان ثبت سفارش"
    
    class Meta : 
        verbose_name = "عنوان ثبت سفارش"
        verbose_name_plural = "عنوان ثبت سفارش"


# نحوه ثبت سفارش
class OrderingGuide(Item) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    about = models.ForeignKey(AboutUs,on_delete=models.CASCADE,related_name="ordering_items")

    class Meta : 
        verbose_name = "نحوه ثبت سفارش"
        verbose_name_plural = "راهنمای سفارش"

# عنوان سوالات متداول
class FeqTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    about = models.OneToOneField(AboutUs,on_delete=models.CASCADE,related_name="feq_title")

    title = models.CharField(max_length=256,null=True,blank=True,verbose_name="عنوان سوالات متداول")

    icon = models.ImageField(upload_to="config/aboute/feq/",null=True,blank=True,verbose_name="ایکون")

    def __str__(self) : 
        return "عنوان سوالات متداول"
    
    class Meta : 
        verbose_name = "عنوان سوالات متداول"
        verbose_name_plural = "عنوان سوالات متداول"

# سوالات متداول
class Feq(Item) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    about = models.ForeignKey(AboutUs,on_delete=models.CASCADE,related_name="feqs")

    class Meta : 
        verbose_name = "سوال "
        verbose_name_plural = "سوالات متداول"

# صفحه تماس با ما
class ContactUs (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    background_title = models.CharField(max_length=256,null=True,blank=True,verbose_name="عنوان روی بک گراند")

    background = models.ImageField(upload_to="config/contact-us/background/",null=True,blank=True,verbose_name="بک گراند")

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

    icon = models.ImageField(upload_to="config/contact-us/icon/",verbose_name="آیکون عنوان",null=True,blank=True)

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

    icon = models.ImageField(upload_to="config/socials/",null=True,blank=True,verbose_name="ایکون")

    def __str__(self) : 
        return "عنوان شبکه های اجتماعی"
    
    class  Meta : 
        verbose_name = "عنوان شبکه های اجتماعی"
        verbose_name_plural = "مدیرت عنوان شبکه های اجتماعی"

# شبکه های اجتماعی
class SocialContact(models.Model) : 

    contact = models.ForeignKey(ContactUs,on_delete=models.CASCADE,related_name="contact_social")

    icon = models.ImageField(upload_to="config/socials/",verbose_name="آیکون")

    url = models.URLField(verbose_name="آدرس")

    def __str__(self) : 
        return "social contact"
    
    class Meta : 
        verbose_name = "شبکه اجتماعی"
        verbose_name_plural = "شبکه های اجتماعی"