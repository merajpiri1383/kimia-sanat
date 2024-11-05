from django.db import models
from uuid import uuid4
from django.utils.text import slugify
from utils.models import Item,CommentBase
from user.models import Ip
from django_jalali.db.models import jDateField
from django.contrib.auth import get_user_model
from django.conf import settings


# مدل استاندارد
class Standard (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    name = models.CharField(max_length=256,verbose_name="نام استاندارد")

    image = models.ImageField(upload_to="product/standard/image/",verbose_name="تصویر استاندارد")

    text = models.TextField(verbose_name="توضیحات استاندارد",null=True,blank=True)

    def __str__(self):
        return str(self.name)

    class Meta :
        verbose_name = "استاندارد"
        verbose_name_plural = "استاندارد ها"
        ordering =["id"]


# مدل دسته بندی محصول
class Category (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    name = models.CharField(max_length=256,verbose_name="نام دسته بندی",unique=True)

    slug = models.SlugField(null=True,blank=True,allow_unicode=True)
    
    description = models.TextField(verbose_name="توضیحات دسته بندی")

    def __str__(self):
        return str(self.name)

    class Meta :
        verbose_name = "دسته بندی محصول"
        verbose_name_plural = "دسته بندی های محصول"

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name,allow_unicode=True)
        return super().save(*args,**kwargs)



types_of_product = [
    ('pasty','خمیری'),
    ('fluid','مایع'),
    ('powdery','پودری')
]

# مدل محصول
class Product (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    category = models.ForeignKey(
        to = Category,
        on_delete = models.CASCADE,
        related_name = "products",
        verbose_name = "دسته بندی"
    )

    video = models.FileField(
        upload_to="product/video/",
        verbose_name="ویدیو",
        null=True,
        blank=True,
    )

    image = models.ImageField(
        upload_to="product/images/",
        verbose_name="تصویر شاخص",
        null=True,
        blank=True
    )

    code = models.SlugField(verbose_name="کد محصول",max_length=20)

    title = models.CharField(max_length=256,verbose_name="عنوان محصول",unique=True)

    slug = models.SlugField(null=True,blank=True,allow_unicode=True)

    type = models.CharField(max_length=10,choices=types_of_product,default="fluid",verbose_name="نوع محصول")

    liked = models.ManyToManyField(
        to = get_user_model(),
        blank = True , 
        related_name = "products_liked"
    )

    views = models.ManyToManyField(Ip)

    description = models.TextField(verbose_name="توضیحات محصول")

    maintain_description = models.TextField(verbose_name="روند نگهداری محصول",null=True,blank=True)

    consumtion_order = models.TextField(verbose_name="روش مصرف",blank=True,null=True)

    standard = models.ManyToManyField(
        to = Standard ,
        verbose_name = "استاندارد ها",
        blank=True
    )

    packing_description = models.TextField(verbose_name="بسته بندی محصول",null=True,blank=True)

    catalog_url = models.CharField(max_length=256,verbose_name='آدرس کاتالوگ',null=True,blank=True)

    catalog_file = models.FileField(verbose_name="فایل کاتالوگ",null=True,blank=True)

    created = jDateField(auto_now_add=True)

    class Meta :
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.category} - {self.title}"

    def save(self,**kwargs):
        self.slug = slugify(self.title,allow_unicode=True)

        if not self.catalog_url and self.catalog_file : 
            self.catalog_url = f"{settings.MEDIA_URL}{self.catalog_file}"
        return super().save(**kwargs)
    
    def index (self) : 
        return list(Product.objects.all()).index(self) + 1
    
    index.short_description = "ردیف"


# مدل ویژگی محصول
class FeatureProduct(Item):

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    product = models.ForeignKey(
        to = Product,
        on_delete = models.CASCADE,
        related_name = "features",
        verbose_name="محصول"
    )

    value = models.CharField(max_length=256,verbose_name="مقدار")

    class Meta :
        verbose_name = "مشخصات فیزیکی و شیمیای محصول"
        verbose_name_plural = "مشخصات فیزیکی و شیمیای محصول"



# مدل کاربرد محصول

class UsageProduct (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    product = models.ForeignKey(
        to = Product,
        on_delete = models.CASCADE,
        related_name = "usages",
        verbose_name="محصول"
    )

    value = models.CharField(verbose_name="کاربرد",max_length=256)

    def __str__(self):
        return str(self.value)

    class Meta :
        verbose_name = "کاربرد محصول"
        verbose_name_plural = "کاربرد های محصول"


# مدل تصویر محصول

class ImageProduct (models.Model) :

    id = models.UUIDField(default=uuid4, primary_key=True, unique=True)

    product = models.ForeignKey(
        to = Product,
        on_delete = models.CASCADE,
        related_name="images",
        verbose_name="محصول"
    )

    image = models.ImageField(upload_to="product/images/",verbose_name="تصویر")

    def __str__(self):
        return str(self.product.title)

    class Meta :
        verbose_name = "تصویر محصول"
        verbose_name_plural = 'تصاویر محصول'


# مدل کامنت
class Comment (CommentBase) :

    product = models.ForeignKey(
        to = Product,
        on_delete = models.CASCADE,
        related_name = "comments",
        verbose_name = "محصول"
    )

    email = models.EmailField(verbose_name="ایمیل",null=True,blank=True)

    liked_by = models.ManyToManyField(
        to=get_user_model(),
        blank=True,
        related_name="product_comment_likeds",
        verbose_name="لایک شده توسط"
    )

    disliked_by = models.ManyToManyField(
        to=get_user_model(),
        blank=True,
        verbose_name="دیس لایک شده توسط",
        related_name="product_comment_dislikeds"
    )
    
    class Meta :
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت های محصولات"
        ordering = ["-created"]


# مدل گزارش تخلف
class ViolationComment (models.Model) :

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    comment = models.ForeignKey(
        to = Comment , 
        on_delete = models.CASCADE , 
        related_name = "violations",
        verbose_name = "کامنت"
    )

    topic = models.CharField(max_length=256,verbose_name="موضوع")

    description = models.TextField(verbose_name="توضیحات")

    def __str__ (self) : 
        return str(self.topic)
    
    class Meta : 
        verbose_name = "گزارش تخلف کامنت"
        verbose_name_plural = "گزارشات تخلف کامنت ها"