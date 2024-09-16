from django.db import models
from uuid import uuid4
from django_jalali.db.models import jDateTimeField

# مدل قالب سایت 
class Template (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)


    logo = models.ImageField(upload_to="template/logo/",verbose_name="لوگو سایت",null=True,blank=True)

    phone = models.SlugField(verbose_name="شماره تلفن داخل هدر",null=True,blank=True)

    email = models.EmailField(verbose_name="ایمیل داخل هدر",null=True,blank=True)

    def __str__(self) : 
        return "قالب"
    
    class Meta : 
        verbose_name = 'قالب'
        verbose_name_plural = 'مدیرت قالب'


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

    template = models.OneToOneField(
        to = Template,
        on_delete= models.CASCADE,
        related_name= "comming_soon"
    )

    title = models.CharField(max_length=256,verbose_name="عنوان صفحه",null=True,blank=True)

    background_image = models.ImageField(upload_to="template/commingsoon/",verbose_name="بک گراند صفحه")

    time = jDateTimeField(null=True,blank=True,verbose_name="زمان")

    is_active = models.BooleanField(default=False,verbose_name="فعال است")

    def __str__(self) : 
        return str(self.title)
    
    class Meta : 
        verbose_name = "صفحه بزودی"
        verbose_name_plural = "مدیرت صفحه بزودی"


# مدل عنوان محصولات
class ProductTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    template = models.OneToOneField(
        to = Template,
        on_delete= models.CASCADE,
        related_name= "product_title"
    )

    title = models.CharField(max_length=256,verbose_name="عنوان محصولات")

    text = models.CharField(max_length=256,null=True,blank=True,verbose_name="عنوان زیر محصولات")

    def __str__(self) : 
        return str(self.title)
    
    class Meta : 
        verbose_name = "عنوان صفحه محصولات"
        verbose_name_plural = "مدیرت عنوان صفحه محصولات"



# مدل عنوان پاسخ به سوالات 
class AnswerQuestionTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    template = models.OneToOneField(
        to = Template,
        on_delete= models.CASCADE,
        related_name= "answe"
    )

    title = models.CharField(max_length=256,verbose_name="عنوان فرم تماس")

    sub_title = models.CharField(max_length=256,verbose_name="عنوان پایینی فرم تماس")

    image = models.ImageField(verbose_name="تصویر کادر زرد",upload_to="answer/image/",null=True,blank=True)

    text = models.TextField(null=True,blank=True,verbose_name="متن کادر زرد")

    phone_1 = models.PositiveBigIntegerField(verbose_name="شماره تماس ۱",null=True,blank=True)

    phone_2 = models.PositiveBigIntegerField(verbose_name="شماره تماس ۲",null=True,blank=True)

    phone_3 = models.PositiveBigIntegerField(verbose_name="شماره تماس ۳",null=True,blank=True)



# مدل عنوان دستاورد های ما 
class AchievementTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    template = models.OneToOneField(
        to = Template,
        on_delete= models.CASCADE,
        related_name= "achievement_title"
    )

    title = models.CharField(max_length=256,verbose_name="عنوان دستاورد های ما ")

    sub_title = models.CharField(max_length=256,verbose_name="عنوان زیر ")

    def __str__(self) : 
        return str(self.title)
    
    class Meta : 
        verbose_name = "عنوان دستاورد"
        verbose_name_plural = "مدیریت عنوان دستاورد ها"


# مدل عنوان پروژه ها

class ProjectTitle (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    template = models.OneToOneField(
        to = Template,
        on_delete= models.CASCADE,
        related_name= "project_title"
    )

    title = models.CharField(max_length=256,verbose_name="عنوان پروژه ها ")

    sub_title = models.CharField(max_length=256,verbose_name="عنوان کامنت مشتری ")

    def __str__(self) : 
        return str(self.title)
    
    class Meta : 
        verbose_name ="عنوان پروژه"
        verbose_name_plural = "مدیرت عنوان پروژه "


# مدل کامنت مشتری

class CommnetTemplate (models.Model) : 

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    profile_user = models.ImageField(upload_to="template/commnet/profile/",verbose_name="پروفایل کاربر")

    username = models.CharField(max_length=256,verbose_name="نام مشتری")

    position = models.CharField(max_length=256,verbose_name="سمت مشتری")

    text = models.TextField(verbose_name="نظر مشتری")

    def __str__(self) : 
        return str(self.username)
    
    class Meta : 
        verbose_name = "کامنت "
        verbose_name_plural = "مدیرت کامنت ها"


# مدل عنوان مقاله 
class BlogTitle (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    template = models.OneToOneField(
        to = Template,
        on_delete= models.CASCADE,
        related_name= "blog_title"
    )

    title = models.CharField(max_length=256,verbose_name="عنوان مقاله")

    sub_title = models.CharField(max_length=256,verbose_name="زیر عنوان مقاله")

    def __str__(self) :
        return str(self.title)
    
    class Meta : 
        verbose_name = "عنوان بلاگ"
        verbose_name_plural = "مدیرت عنوان بلاگ"