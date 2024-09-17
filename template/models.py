from django.db import models
from uuid import uuid4
from django_jalali.db.models import jDateTimeField

class Header (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    logo = models.ImageField(upload_to="header/logo/",verbose_name="لوگو سایت",null=True,blank=True)

    phone = models.SlugField(verbose_name="شماره تلفن داخل هدر",null=True,blank=True)

    email = models.EmailField(verbose_name="ایمیل داخل هدر",null=True,blank=True)

    icon = models.ImageField(upload_to="header/icon/",verbose_name="آیکون کنار شماره و ایمیل در هدر",null=True,blank=True)

    def __str__(self) : 
        return "هدر"
    
    class Meta : 
        verbose_name ="هدر"
        verbose_name_plural = "مدیرت هدر"

# مدل منو
class Menu (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    name = models.CharField(max_length=256,verbose_name="نام منو")

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

    def __str__(self) : 
        return str(self.name)
    
    class Meta : 
        verbose_name = "زیر منو"
        verbose_name_plural = "زیر منو ها"


# مدل کامینگ سون
class CommingSoon (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    title = models.CharField(max_length=256,verbose_name="عنوان صفحه",null=True,blank=True)

    background_image = models.ImageField(upload_to="template/commingsoon/",verbose_name="بک گراند صفحه",null=True,blank=True)

    time = jDateTimeField(null=True,blank=True,verbose_name="زمان")

    is_active = models.BooleanField(default=False,verbose_name="فعال است")

    def __str__(self) : 
        return "صفحه comming soon"
    
    class Meta : 
        verbose_name = "Comming Soon"
        verbose_name_plural = "مدیرت Comming Soon"


# مدل عنوان محصولات
class ProductTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    title = models.CharField(max_length=256,verbose_name="عنوان محصولات",null=True,blank=True)

    sub_title = models.CharField(max_length=256,null=True,blank=True,verbose_name="عنوان زیر محصولات")

    def __str__(self) : 
        return str(self.title)
    
    class Meta : 
        verbose_name = "عنوان صفحه محصولات"
        verbose_name_plural = "مدیرت عنوان صفحه محصولات"




# مدل عنوان پاسخ به سوالات 
class AnswerQuestionTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    title = models.CharField(max_length=256,verbose_name="عنوان فرم تماس",null=True,blank=True)

    sub_title = models.CharField(max_length=256,verbose_name="عنوان پایینی فرم تماس",null=True,blank=True)

    image = models.ImageField(verbose_name="تصویر کادر زرد",upload_to="answer/image/",null=True,blank=True)

    text = models.TextField(null=True,blank=True,verbose_name="متن کادر زرد")

    phone_1 = models.PositiveBigIntegerField(verbose_name="شماره تماس ۱",null=True,blank=True)

    phone_2 = models.PositiveBigIntegerField(verbose_name="شماره تماس ۲",null=True,blank=True)

    phone_3 = models.PositiveBigIntegerField(verbose_name="شماره تماس ۳",null=True,blank=True)

    def __str__(self) : 
        return "مدیرت سوالات  مشتری"
    
    class Meta : 
        verbose_name = "مدیرت سوالات مشتری"
        verbose_name_plural = "مدیرت سوالات مشتری"




# مدل عنوان دستاورد های ما 
class AchievementTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    title = models.CharField(max_length=256,verbose_name="عنوان دستاورد های ما ",null=True,blank=True)

    sub_title = models.CharField(max_length=256,verbose_name="عنوان زیر ",null=True,blank=True)

    def __str__(self) : 
        return str(self.title)
    
    class Meta : 
        verbose_name = "عنوان دستاورد"
        verbose_name_plural = "مدیریت عنوان دستاورد ها"


# مدل عنوان مقاله 
class BlogTitle (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    title = models.CharField(max_length=256,verbose_name="عنوان مقاله",null=True,blank=True)

    sub_title = models.CharField(max_length=256,verbose_name="زیر عنوان مقاله",null=True,blank=True)

    def __str__(self) :
        return str(self.title)
    
    class Meta : 
        verbose_name = "عنوان بلاگ"
        verbose_name_plural = "مدیرت عنوان بلاگ"


# مدل عنوان پروژه ها

class ProjectTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)


    title = models.CharField(max_length=256,verbose_name="عنوان پروژه ها ",null=True,blank=True)

    sub_title = models.CharField(max_length=256,verbose_name="عنوان کامنت مشتری ",null=True,blank=True)

    def __str__(self) : 
        return str(self.title)
    
    class Meta : 
        verbose_name = " عنوان پروژه و زیر عنوان"
        verbose_name_plural = "مدیرت عنوان پروژه ها"

class Comment (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    project = models.ForeignKey(ProjectTitle,on_delete=models.CASCADE,related_name="comments")

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

    title_slider = models.CharField(max_length=256,verbose_name="عنوان اسلایدر",null=True,blank=True)

    text_slider = models.TextField(null=True,blank=True,verbose_name="متن اسلایدر")

    short_description = models.TextField(null=True,blank=True,verbose_name="توضیحات مختصر و مفید")

    link_slider = models.URLField(null=True,blank=True,verbose_name='لینک دکمه اطلاعات بیشتر')

    def __str__(self) : 
        return "اسلایدر"
    
    class Meta : 
        verbose_name = "اسلایدر صفحه هوم"
        verbose_name_plural = "مدیرت اسلایدر صفحه هوم"



class ImageSlider (models.Model ) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    slider = models.ForeignKey(
        to = Slider,
        on_delete = models.CASCADE,
        related_name = "images"
    )

    image = models.ImageField(upload_to="company/images/",verbose_name="تصویر")

    def __str__ (self) : 
        return "image"
    
    class Meta : 
        verbose_name = "تصویر اسلایدر "
        verbose_name_plural = "تصاویر اسلایدر "


class FirstPageContent (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    title = models.CharField(max_length=256,verbose_name="عنوان گواهینامه",null=True,blank=True)

    sub_title = models.CharField(max_length=256,verbose_name="زیر عنوان گواهینامه",null=True,blank=True)

    side_image = models.ImageField(upload_to="first_page_content/side_image/",verbose_name="عکس کنار گواهینامه ")

    pattern_image = models.ImageField(upload_to="first_page_content/pattern_image/",verbose_name="عکس پترن",null=True,blank=True)

    def __str__ (self) : 
        return "محتوای صفحه اول"
    
    class Meta : 
        verbose_name = "محتوای صفحه اول"
        verbose_name_plural = "مدیرت محتوای صفحه اول"

# گواهینامه ها
class License (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    content_page = models.ForeignKey(
        to = FirstPageContent,
        on_delete = models.CASCADE,
        related_name="licenses"
    )

    title = models.CharField(max_length=256,verbose_name="عنوان")

    logo = models.ImageField(upload_to="home/license/logo/",verbose_name="لوگو گواهینامه")

    sub_title = models.CharField(max_length=256,verbose_name="زیر عنوان")

    def __str__(self) : 
        return str(self.title)
    
    class Meta : 
        verbose_name = "گواهی نامه"
        verbose_name_plural = "گواهی نامه ها"