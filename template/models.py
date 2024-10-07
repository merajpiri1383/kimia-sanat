from django.db import models
from uuid import uuid4
from django_jalali.db.models import jDateTimeField
from blog.models import Blog
from project.models import Category as CategoryProject
from utils.models import Item
from product.models import Category as CategoryProduct
from django.core.exceptions import ValidationError
import re

class Header (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    logo = models.ImageField(upload_to="header/logo/",verbose_name="لوگو سایت",null=True,blank=True)

    phone = models.SlugField(verbose_name="شماره تلفن داخل هدر",null=True,blank=True)

    email = models.EmailField(verbose_name="ایمیل داخل هدر",null=True,blank=True)

    # icon = models.ImageField(verbose_name="آیکون کنار شماره و ایمیل در هدر",null=True,blank=True)


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

    internal_url = models.URLField(null=True,blank=True,verbose_name="لینک داخلی")

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

    interal_url = models.URLField(null=True,blank=True,verbose_name="لینک داخلی ")

    external_url = models.URLField(null=True,blank=True,verbose_name="لینک خارجی")

    def __str__(self) : 
        return str(self.name)
    
    class Meta : 
        verbose_name = "زیر منو"
        verbose_name_plural = "زیر منو ها"


# مدل کامینگ سون
class CommingSoon (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    logo = models.ImageField(upload_to="template/commingsoon/logo/",verbose_name="لوگو",null=True,blank=True)

    title = models.CharField(max_length=256,verbose_name="عنوان صفحه",null=True,blank=True)

    sub_title = models.CharField(max_length=256,blank=True,null=True,verbose_name="زیر عنوان")

    background_image = models.ImageField(upload_to="template/commingsoon/",verbose_name="بک گراند صفحه",null=True,blank=True)

    time = jDateTimeField(null=True,blank=True,verbose_name="زمان")

    copy_right_text = models.TextField(null=True,blank=True,verbose_name="متن کپی رایت")

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

    # icon = models.ImageField(max_length=256,null=True,blank=True,verbose_name="ایکون کادر")

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

    # icon = models.ImageField(max_length=256,null=True,blank=True,verbose_name="ایکون ")

    box_title = models.CharField(max_length=256,verbose_name="عنوان باکس",null=True,blank=True)

    box_text = models.TextField(null=True,blank=True,verbose_name="متن باکس")

    image = models.ImageField(verbose_name="تصویر کادر زرد",upload_to="answer/image/",null=True,blank=True)

    text = models.TextField(null=True,blank=True,verbose_name="متن کادر زرد")

    # icon_phone = models.ImageField(max_length=256,verbose_name="آیکون قسمت شماره ها",null=True,blank=True)

    def __str__(self) : 
        return "مدیرت سوالات  مشتری"
    
    class Meta : 
        verbose_name = "مدیرت سوالات مشتری"
        verbose_name_plural = "مدیرت باکس درخواست مشاوره"

class PhoneAnswerQuestion (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    card = models.ForeignKey(AnswerQuestionTitle,on_delete=models.CASCADE,related_name="phones")

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

    # icon = models.ImageField(max_length=256,verbose_name="ایکون",null=True,blank=True)

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

    # icon = models.ImageField(max_length=256,verbose_name="ایکون کادر مقاله",null=True,blank=True)

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

    # icon = models.ImageField(max_length=256,verbose_name="ایکون کادر پروژه ها",null=True,blank=True)

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

    pattern_image = models.ImageField(upload_to="first_page_content/pattern_image/",verbose_name="عکس پترن",null=True,blank=True)

    def __str__ (self) : 
        return "محتوای صفحه اول"
    
    class Meta : 
        verbose_name = "محتوای صفحه اول"
        verbose_name_plural = "مدیرت محتوای صفحه اول"


# فوتر 

class Footer (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    logo = models.ImageField(upload_to="template/footer/logo/",verbose_name="لوگو ",null=True,blank=True)

    text = models.TextField(null=True,blank=True,verbose_name="متن فوتر")

    link_footer_title = models.CharField(max_length=256,verbose_name="عنوان ستون لینک ها",null=True,blank=True)

    category_footer_title = models.CharField(max_length=128,null=True,blank=True,verbose_name="عنوان ستون دسته بندی ها")

    copyright_text = models.TextField(verbose_name="متن کپی رایت",null=True,blank=True)

    def __str__ (self) : 
        return "فوتر"
    
    class Meta : 
        verbose_name = "فوتر"
        verbose_name_plural = "فوتر"


class PhoneFooter (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    footer = models.ForeignKey(Footer,on_delete=models.CASCADE,related_name="footer_phones")

    # icon = models.ImageField(max_length=256,null=True,blank=True,verbose_name="آیکون")

    phone = models.CharField(max_length=256,verbose_name="شماره")

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

class SocialFooter (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    footer = models.ForeignKey(Footer,on_delete=models.CASCADE,related_name="footer_socials")

    # icon = models.ImageField(max_length=256,null=True,blank=True,verbose_name="آیکون")

    url = models.URLField(verbose_name="آدرس")

    def __str__ (self) : 
        return "شبکه اجتماعی فوتر"
    
    class Meta : 
        verbose_name = "شبکه اجتماعی فوتر"
        verbose_name_plural = "شبکه های اجتماعی فوتر"
    
class FooterLink (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    footer = models.ForeignKey(Footer,on_delete=models.CASCADE,related_name="footer_links")

    name = models.CharField(max_length=256,verbose_name="نام لینک")

    internal_url = models.URLField(verbose_name="ادرس داخلی",null=True,blank=True)

    external_url = models.URLField(verbose_name="ادرس خارجی",null=True,blank=True)

    def __str__ (self) : 
        return str(self.name)
    
    class Meta : 
        verbose_name = "لینک فوتر"
        verbose_name_plural = "لینک های فوتر"

class CategoryFooter (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    footer = models.ForeignKey(Footer,on_delete=models.CASCADE,related_name="footer_category")

    name = models.CharField(max_length=256,verbose_name="نام دسته بندی")

    url = models.URLField(verbose_name="آدرس دسته بندی")

    def __str__(self) : 
        return str (self.name)
    
    class Meta : 
        verbose_name = "دسته بندی فوتر"
        verbose_name_plural = "دسته بندی های فوتر "


regex_phone = re.compile("^0[0-9]{10}$")

persons = (
    ('real','حقیقی'),
    ('legal','حقوقی'),
)

class Consult (models.Model ) : 
    
    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    name = models.CharField(max_length=256,verbose_name="نام و نام خانوادگی")

    person = models.CharField(max_length=5,choices=persons,default="real")

    phone = models.SlugField(max_length=11,verbose_name="شماره همراه")

    email = models.EmailField(verbose_name="ایمیل")

    text = models.TextField(verbose_name="توضیحات")

    is_valid = models.BooleanField(default=False,verbose_name="تایید شده توسط ادمین")

    def __str__(self) : 
        return  str(self.name)
    
    class Meta : 
        verbose_name = "درخواست مشاوره "
        verbose_name_plural = 'درخواست های مشاوره کاربران'
    
    def clean(self) : 
        if not regex_phone.findall(self.phone) : 
            raise ValidationError("phone must be integer and 11 character .")

# مدل باشگاه مشتریان 
class CustomerClub (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    phone = models.SlugField(verbose_name="شماره")

    def __str__ (self) : 
        return str(self.phone)
    
    class Meta : 
        verbose_name = "مشتری"
        verbose_name_plural = "باشگاه مشتریان"
    
    def clean(self) : 

        if not regex_phone.findall(self.phone) : 
            raise ValidationError("invalid phone number .")