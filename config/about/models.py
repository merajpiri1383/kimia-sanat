from django.db import models
from uuid import uuid4
from utils.models import Item
from project.models import Project

# صفحه درباره ما 
class AboutUs (models.Model) : 

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

    # icon = models.ImageField(max_length=256,verbose_name="ایکون",null=True,blank=True)

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

    def __str__(self) : 
        return "عنوان سوالات متداول"
    
    class Meta : 
        verbose_name = "عنوان سوالات متداول"
        verbose_name_plural = "عنوان سوالات متداول"

# سوالات متداول
class Feq(models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    about = models.ForeignKey(AboutUs,on_delete=models.CASCADE,related_name="feqs")

    question = models.TextField(verbose_name="سوال", null=True)

    answer = models.TextField(verbose_name="جواب", null=True)

    def __str__(self) -> str:
        return "سوال"

    class Meta : 
        verbose_name = "سوال "
        verbose_name_plural = "سوالات متداول"

# فرم ارتباط با ما در صفحه ارتباط با ما 

class ContactConsult (models.Model) : 

    CHOICES_FIELDS = (
        ("legal", "حقوقی"),
        ("personal", "حقیقی")
    )

    id = models.UUIDField(unique=True,primary_key=True,default=uuid4)

    name = models.CharField(verbose_name="نام", max_length=100)
    
    department = models.CharField(max_length=256,verbose_name="دپارتمان", choices=CHOICES_FIELDS)

    phone = models.SlugField(verbose_name="شماره تلفن")

    email = models.EmailField(verbose_name="ایمیل")

    text = models.TextField(verbose_name="توضیحات")

    def __str__(self) : 
        return str (self.name)
    
    class Meta : 
        verbose_name = "درخواست مشاوره "
        verbose_name_plural = "درخواست های تماس با ما"