from django.db import models
from uuid import uuid4
from blog.models import Blog
from project.models import Category as CategoryProject
from utils.models import Item
from product.models import Category as CategoryProduct
from django.core.exceptions import ValidationError
import re


regex_phone = re.compile("^0[0-9]{10}$")



# مدل عنوان محصولات
class ProductTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    title = models.CharField(max_length=256,verbose_name="عنوان محصولات",null=True,blank=True)

    sub_title = models.CharField(max_length=256,null=True,blank=True,verbose_name="عنوان زیر محصولات")

    button_text = models.CharField(max_length=128,null=True,blank=True,verbose_name="متن button")

    button_url = models.URLField(null=True,blank=True,verbose_name="آدرس button")

    categories = models.ManyToManyField(CategoryProduct,blank=True,verbose_name="دسته بندی های محصول")

    def __str__(self) : 
        return str(self.title)
    
    class Meta : 
        verbose_name = "کادر محصولات"
        verbose_name_plural = "مدیرت کادر محصولات"




# مدل عنوان پاسخ به سوالات 
class AnswerQuestionTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    title = models.CharField(max_length=256,verbose_name="عنوان فرم تماس",null=True,blank=True)

    sub_title = models.CharField(max_length=256,verbose_name="عنوان پایینی فرم تماس",null=True,blank=True)

    box_title = models.CharField(max_length=256,verbose_name="عنوان باکس",null=True,blank=True)

    box_text = models.TextField(null=True,blank=True,verbose_name="متن باکس")

    image = models.ImageField(verbose_name="تصویر کادر زرد",upload_to="answer/image/",null=True,blank=True)

    text = models.TextField(null=True,blank=True,verbose_name="متن کادر زرد")

    def __str__(self) : 
        return "مدیرت سوالات  مشتری"
    
    class Meta : 
        verbose_name = "مدیرت سوالات مشتری"
        verbose_name_plural = "مدیرت باکس درخواست مشاوره"

class PhoneAnswerQuestion (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    card = models.ForeignKey(AnswerQuestionTitle,on_delete=models.CASCADE,related_name="phones")

    title = models.CharField(max_length=256,verbose_name="عنوان",null=True,blank=True)

    phone = models.CharField(max_length=11,verbose_name="شماره تلفن")

    def __str__ (self) : 
        return str(self.phone)

    class Meta : 
        verbose_name = 'شماره'
        verbose_name_plural = "شماره ها"


# مدل عنوان دستاورد های ما 
class AchievementCard (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    title = models.CharField(max_length=256,verbose_name="عنوان دستاورد های ما ",null=True,blank=True)

    sub_title = models.CharField(max_length=256,verbose_name="عنوان زیر ",null=True,blank=True)

    def __str__(self) : 
        return str(self.title)
    
    class Meta : 
        verbose_name = "کادر دستاورد"
        verbose_name_plural = "مدیریت کادر دستاورد ها"

class AchievementCardItem (Item) :

    achievement = models.ForeignKey(AchievementCard,on_delete=models.CASCADE,related_name="items")

    class Meta : 
        verbose_name = "دستاورد"
        verbose_name_plural = 'دستاورد ها'

# مدل عنوان مقاله 
class BlogTitle (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    title = models.CharField(max_length=256,verbose_name="عنوان مقاله",null=True,blank=True)

    sub_title = models.CharField(max_length=256,verbose_name="زیر عنوان مقاله",null=True,blank=True)

    button_text = models.CharField(max_length=128,null=True,blank=True,verbose_name="متن button")

    button_url = models.CharField(max_length=128,null=True,blank=True,verbose_name="آدرس button")

    blogs = models.ManyToManyField(Blog,blank=True,verbose_name="مقاله ها")

    def __str__(self) :
        return str(self.title)
    
    class Meta : 
        verbose_name = "کادر بلاگ"
        verbose_name_plural = "مدیرت کادر بلاگ"


# مدل عنوان پروژه ها

class ProjectTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    title = models.CharField(max_length=256,verbose_name="عنوان پروژه ها ",null=True,blank=True)

    sub_title = models.CharField(max_length=256,verbose_name="عنوان کامنت مشتری ",null=True,blank=True)

    button_text = models.CharField(max_length=128,null=True,blank=True,verbose_name="متن button")

    button_url = models.URLField(null=True,blank=True,verbose_name="آدرس button")

    category_projects = models.ManyToManyField(CategoryProject,blank=True,verbose_name="دسته بندی های پروژه")

    def __str__(self) : 
        return str(self.title)
    
    class Meta : 
        verbose_name = " کادر پروژه"
        verbose_name_plural = "مدیرت کادر پروژه ها"

class Comment (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    project = models.ForeignKey(ProjectTitle,on_delete=models.CASCADE,related_name="comments")

    title = models.CharField(max_length=256,verbose_name="عنوان کامنت",null=True,blank=True)

    profile_user = models.ImageField(upload_to="template/commnet/profile/",verbose_name="پروفایل کاربر")

    username = models.CharField(max_length=256,verbose_name="نام مشتری")

    position = models.CharField(max_length=256,verbose_name="سمت مشتری")

    text = models.TextField(verbose_name="نظر مشتری")

    def __str__(self) : 
        return str(self.username)
    
    class Meta : 
        verbose_name = "کامنت مشتری "
        verbose_name_plural = "مدیرت کامنت های مشتری "


class Slider (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    title = models.CharField(max_length=256,verbose_name="عنوان",null=True,blank=True)

    sub_title = models.CharField(max_length=256,verbose_name="عنوان پایین",null=True,blank=True)

    text = models.TextField(null=True,blank=True,verbose_name="متن اسلاید")

    image = models.ImageField(upload_to="template/slider/image/",verbose_name="تصویر اسلاید")

    button_text = models.CharField(max_length=128,verbose_name="متن button",null=True,blank=True)

    link_slider = models.URLField(null=True,blank=True,verbose_name='لینک دکمه اطلاعات بیشتر')

    def __str__(self) : 
        return "اسلایدر"
    
    class Meta : 
        verbose_name = "اسلایدر"
        verbose_name_plural = "مدیرت اسلایدر"


class AchievementTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    title = models.CharField(max_length=256,verbose_name="عنوان",null=True,blank=True)

    # icon = models.ImageField(max_length=128,unique=True,blank=True,verbose_name="آیکون")

    text = models.TextField(null=True,blank=True,verbose_name="متن")

    def __str__(self) : 
        return "پاپ آپ دستاورد ها"
    
    class Meta : 
        verbose_name = "پاپ آپ دستاورد ها"
        verbose_name_plural = "مدیریت پاپ آپ دستاورد ها"


# دستاورد ها
class Achievement (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    card = models.ForeignKey(
        to = AchievementTitle , 
        on_delete = models.CASCADE,
        related_name="items"
    )

    title = models.CharField(max_length=256,verbose_name="عنوان")

    logo = models.ImageField(upload_to="home/license/logo/",verbose_name="لوگو گواهینامه")

    text = models.TextField(verbose_name="متن دستاورد")

    def __str__(self) : 
        return str(self.title)
    
    class Meta : 
        verbose_name = "دستاورد  "
        verbose_name_plural = "دستاورد"

class FirstPageContent (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    title = models.CharField(max_length=256,verbose_name="عنوان گواهینامه",null=True,blank=True)

    sub_title = models.CharField(max_length=256,verbose_name="زیر عنوان گواهینامه",null=True,blank=True)

    side_image = models.ImageField(upload_to="first_page_content/side_image/",verbose_name="عکس کنار گواهینامه ")

    button_text = models.CharField(max_length=128,verbose_name="متن button",null=True,blank=True)

    achievements = models.ManyToManyField(
        to = Achievement , 
        blank=True,
        verbose_name="دستاورد ها "
    )

    def __str__ (self) : 
        return "گواهینامه های صفحه اصلی"
    
    class Meta : 
        verbose_name = "گواهینامه های صفحه اصلی"
        verbose_name_plural = "گواهینامه های صفحه اصلی"


persons = (
    ('real','حقیقی'),
    ('legal','حقوقی'),
)

class Consult (models.Model ) : 
    
    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    name = models.CharField(max_length=256,verbose_name="نام و نام خانوادگی")

    person = models.CharField(
        max_length=5,
        choices=persons,
        default="real",
        verbose_name="شخص"
    )

    phone = models.SlugField(max_length=11,verbose_name="شماره همراه")

    email = models.EmailField(verbose_name="ایمیل")

    text = models.TextField(verbose_name="توضیحات")

    is_valid = models.BooleanField(default=False,verbose_name="خوانده شده")

    def __str__(self) : 
        return  str(self.name)
    
    class Meta : 
        verbose_name = "درخواست مشاوره "
        verbose_name_plural = 'درخواست های مشاوره کاربران'
    
    def clean(self) : 
        if not regex_phone.findall(self.phone) : 
            raise ValidationError("phone must be integer and 11 character .")
        