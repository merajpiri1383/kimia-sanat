from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from user.manager import UserManager
from uuid import uuid4
from random import randint
import re
from django.core.exceptions import ValidationError



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

    national_code = models.PositiveBigIntegerField(verbose_name="کد ملی")

    email = models.EmailField(verbose_name="ایمیل")

    national_card = models.ImageField(upload_to="user/real-profile/national-card/",
                                      verbose_name="آپلود کارت ملی")

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

    class Meta :
        verbose_name = "پروفایل حقوقی"
        verbose_name_plural = "پروفایل حقوقی کاربر"

    def __str__(self):
        return f"{self.name}"