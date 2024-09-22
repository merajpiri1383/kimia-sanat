from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from driver.models import Driver
from user.manager import UserManager
from uuid import uuid4
from random import randint
import re
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator,MaxValueValidator
from django_jalali.db.models import jDateField


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

    otp_code = models.SlugField(max_length=5,verbose_name="کد تایید",null=True,blank=True)

    drivers = models.ManyToManyField(to=Driver,blank=True,verbose_name="راننده های کاربر")

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta :
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return str(self.phone)

    def save(self,*args,**kwargs):
        self.clean()
        self.otp_code = randint(10000,99999)
        return super().save(*args,**kwargs)

    def clean(self) :
        if not regex_phone.findall(self.phone) :
            raise ValidationError("phone must be integer , start with 0 and 11 character .")



regex_telephone = re.compile("^[0-9]{5,12}$")

# مدل پایه پروفایل

class ProfileBase (models.Model) :

    address = models.TextField(verbose_name="آدرس پستی")

    postal_code = models.PositiveBigIntegerField(verbose_name="کد پستی")

    telephone = models.SlugField(verbose_name="تلفن ثابت")

    social_phone = models.SlugField(verbose_name="شماره موبایل شبکه اجتماعی")

    social_media = models.ManyToManyField(
        to = SocialMedia,
        verbose_name="شبکه اجتماعی"
    )

    national_id = models.PositiveBigIntegerField(verbose_name="کد ملی")

    email = models.EmailField(verbose_name="ایمیل")

    class Meta :
        abstract = True

    def clean(self):
        if not regex_phone.findall(self.social_phone) :
            raise ValidationError("phone must be integer , start with 0 and 11 character .")

        if not regex_telephone.findall(self.telephone) :
            raise ValidationError("telephone must be integer .")


# پروفایل کاربر حقیقی
class RealProfile ( ProfileBase ) :

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="real_profile"
    )

    name = models.CharField(max_length=256,verbose_name="نام و نام خانوادگی")

    class Meta :
        verbose_name = "پروفایل حقیقی"

    def __str__(self):
        return str(self.name)

# پروفایل حقوقی کاربر
class LegalProfile ( ProfileBase ) :

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="legal_profile"
    )

    name = models.CharField(max_length=256,verbose_name="نام شرکت")

    economic_code = models.SlugField(verbose_name="کد اقتصادی")

    foundation_date = jDateField(null=True,blank=True,verbose_name="سال تاسیس شرکت")

    company_registration_number = models.PositiveBigIntegerField(verbose_name="شماره ثبت شرکت",null=True,blank=True)

    founder_company = models.CharField(max_length=256,verbose_name="نام صاحب شرکت",null=True,blank=True)

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

    authenticated_code = models.SlugField(null=True,blank=True,verbose_name="کد معرف")

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

    percent = models.IntegerField(
        validators=[MaxValueValidator(100),MinValueValidator(0)],
        verbose_name="درصد بازاریاب")

    discount_percent = models.IntegerField(
        validators=[MaxValueValidator(100),MinValueValidator(0)],
        verbose_name="درصد تخفیف بازاریاب",
        null=True,blank=True)

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

    def save(self,**kwargs):
        if not self.authenticated_code :
            try :
                self.authenticated_code = randint(10000,99999)
            except :
                self.authenticated_code = randint(10000,99999)
        return super().save(**kwargs)