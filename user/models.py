from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from driver.models import Driver
from user.manager import UserManager
from uuid import uuid4
from random import randint
import re
from django.core.exceptions import ValidationError




# مدل شبکه اجتماعی بازار یاب
class SocialMedia (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    name = models.CharField(max_length=256,verbose_name="نام شبکه اجتماعی",unique=True)

    def __str__(self):
        return str(self.name)

    class Meta :
        verbose_name = "شبکه اجتماعی"
        verbose_name_plural = "شبکه های اجتماعی"
class Ip (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    ip = models.SlugField(max_length=30)

    

regex_phone = re.compile("^0[0-9]{10}$")


# مدل اصلی کاربر

class User (AbstractBaseUser,PermissionsMixin) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    phone = models.SlugField(unique=True,max_length=11,verbose_name="موبایل")

    is_active = models.BooleanField(default=False,verbose_name="فعال/غیرفعال")

    is_staff = models.BooleanField(default=False,verbose_name="ادمین است / نیست")

    is_superuser = models.BooleanField(default=False)

    is_real = models.BooleanField(default=False,verbose_name="کاربر حقیقی")

    is_legal = models.BooleanField(default=False,verbose_name="حقوقی")

    is_panel_active = models.BooleanField(default=False,verbose_name="پنل فعال است")

    otp_code = models.SlugField(max_length=5,verbose_name="کد تایید",null=True,blank=True)

    send_sms = models.BooleanField(default=False,verbose_name="ارسال sms")

    drivers = models.ManyToManyField(
        to = Driver , 
        blank = True , 
        verbose_name = "راننده ها"
    )

    saved_products = models.ManyToManyField(
        to = "product.Product" , 
        blank = True ,
        verbose_name = "محصولات ذخیره شده"
    )

    saved_blogs = models.ManyToManyField(
        to = "blog.Blog" , 
        blank = True , 
        verbose_name = "بلاگ های ذخیره شده"
    )

    saved_projects = models.ManyToManyField(
        to = "project.Project",
        blank = True ,
        verbose_name = "پروژه های ذخیره شده"
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta :
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return f"{self.username()} - {self.phone}"

    def save(self,*args,**kwargs):
        self.clean()
        self.otp_code = randint(10000,99999)
        return super().save(*args,**kwargs)
    
    @property
    def unread_notifications (self) :
        return self.notifications.filter(read_users=None).count()

    def clean(self) :
        if not regex_phone.findall(self.phone) :
            raise ValidationError("phone must be integer , start with 0 and 11 character .")
        
    def username (self) : 
        if hasattr(self,"legal_profile") : 
            return self.legal_profile.name
        if hasattr(self,"real_profile") : 
            return self.real_profile.name
        return None
    
    def index (self) : 
        return list(User.objects.all()).index(self) + 1
    
    def user_type (self) : 
        if hasattr(self,"real_profile") : 
            return self.real_profile.type
    
    username.short_description = "نام / نام شرکت"
    user_type.short_description = "نوع کاربر حقیقی"
    index.short_description = "ردیف"



regex_telephone = re.compile("^[0-9]{5,12}$")

real_user_types = [
    ("customer","خریدار"),
    ("seller","فروشنده"),
]

# پروفایل کاربر حقیقی
class RealProfile ( models.Model ) :

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="real_profile"
    )

    name = models.CharField(max_length=256,verbose_name="نام و نام خانوادگی")

    national_id = models.PositiveBigIntegerField(verbose_name="کد ملی")

    email = models.EmailField(verbose_name="ایمیل")

    telephone = models.SlugField(verbose_name="تلفن ثابت")

    postal_code = models.PositiveBigIntegerField(verbose_name="کد پستی")

    type = models.CharField(
        max_length=20,
        verbose_name="نوع کاربر",
        choices=real_user_types,
        default="customer"
    )

    address = models.TextField(verbose_name="آدرس پستی")

    profile_image = models.ImageField(
        upload_to="user/profile/image/",
        null=True,
        blank=True,
        verbose_name="تصویر پروفایل"
    )

    class Meta :
        verbose_name = "پروفایل حقیقی"

    def __str__(self):
        return str(self.name)
    
    def clean(self):

        if not regex_telephone.findall(self.telephone) :
            raise ValidationError("telephone must be integer .")

# پروفایل حقوقی کاربر
class LegalProfile ( models.Model ) :

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="legal_profile"
    )

    name = models.CharField(max_length=256,verbose_name="نام شرکت")

    economic_code = models.SlugField(verbose_name="کد اقتصادی")

    email = models.EmailField(verbose_name="ایمیل")

    telephone = models.SlugField(verbose_name="تلفن ثابت")

    postal_code = models.PositiveBigIntegerField(verbose_name="کد پستی")

    national_id_company = models.PositiveBigIntegerField(verbose_name="کد ملی شرکت")

    address = models.TextField(verbose_name="آدرس پستی")

    profile_image = models.ImageField(
        upload_to="user/profile/image/",
        null=True,
        blank=True,
        verbose_name="تصویر پروفایل"
    )

    def clean(self):
        if not regex_telephone.findall(self.telephone) :
            raise ValidationError("telephone must be integer .")

    class Meta :
        verbose_name = "پروفایل حقوقی"
        verbose_name_plural = "پروفایل حقوقی کاربر"

    def __str__(self):
        return f"{self.name}"
    


time_working = [
    ("full-time",'تمام وقت'),
    ("part-time",'پاره وقت'),
]

marketer_type = [
    ("phone",'تلفنی'),
    ("internet",'اینترنتی'),
    ("presence",'حضوری')
]

regex_phone = re.compile("^0[0-9]{10}$")

# مدل بازار یاب
class Marketer (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    name = models.CharField(unique=True,max_length=256,verbose_name="نام و نام خانوادگی")

    image = models.ImageField(upload_to="marketing/marketer/profile/",verbose_name="عکس پروفایل")

    active_phone = models.SlugField(max_length=11,verbose_name="شماره تماس فعال",unique=True)

    social_media = models.ManyToManyField(SocialMedia,verbose_name="شبکه اجتماعی")

    social_phone = models.SlugField(unique=True,max_length=11,verbose_name="شماره شبکه اجتماعی")

    # authenticated_code = models.SlugField(null=True,blank=True,verbose_name="کد معرف")

    time_work = models.CharField(max_length=10,
                                 choices=time_working,
                                 verbose_name="مدت زمان کار",
                                 default="part-time")

    start_time_work = models.TimeField(null=True,blank=True,verbose_name="ساعت شروع کار")

    end_time_work = models.TimeField(null=True,blank=True,verbose_name="ساعت پایان کار")

    type = models.CharField(max_length=10,
                            choices=marketer_type,
                            default="phone",
                            verbose_name="نوع بازاریاب")

    national_id = models.PositiveBigIntegerField(verbose_name="کد ملی")

    # percent = models.IntegerField(
    #     validators=[MaxValueValidator(100),MinValueValidator(0)],
    #     verbose_name="درصد بازاریاب")

    # discount_percent = models.IntegerField(
    #     validators=[MaxValueValidator(100),MinValueValidator(0)],
    #     verbose_name="درصد تخفیف بازاریاب",
    #     null=True,blank=True)

    class Meta :
        verbose_name = "بازاریاب"
        verbose_name_plural = "بازاریاب ها"

    def clean(self):
        if not regex_phone.findall(self.social_phone) :
            raise ValidationError("social_phone must be integer , start with 0 and 11 character .")

        if not regex_phone.findall(self.active_phone) :
            raise ValidationError("active_phone must be integer , start with 0 and 11 character .")

    def __str__(self):
        return str(self.name)

    # def save(self,**kwargs):
    #     if not self.authenticated_code :
    #         try :
    #             self.authenticated_code = randint(10000,99999)
    #         except :
    #             self.authenticated_code = randint(10000,99999)
    #     return super().save(**kwargs)

    def index (self) : 
        return list(Marketer.objects.all()).index(self) + 1
    
    index.short_description = "ردیف"