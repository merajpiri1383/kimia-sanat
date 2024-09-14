from django.db import models
from uuid import uuid4
from django.core.validators import MaxValueValidator,MinValueValidator
from django.core.exceptions import ValidationError
import re

# مدل شبکه اجتماعی بازار یاب
class SocialMedia (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    name = models.CharField(max_length=256,verbose_name="نام شبکه اجتماعی",unique=True)

    def __str__(self):
        return str(self.name)

    class Meta :
        verbose_name = "شبکه اجتماعی"
        verbose_name_plural = "شبکه های اجتماعی"


time_working = [
    ('تمام وقت',"full-time"),
    ('پاره وقت',"part-time"),
]

marketer_type = [
    ('تلفنی',"phone"),
    ('اینترنتی',"internet"),
    ('حضوری',"presence")
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