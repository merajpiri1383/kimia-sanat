from django.db import models
from uuid import uuid4
from django.utils.text import slugify
from utils.models import Item

# مدل استاندارد
class Standard (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    name = models.CharField(max_length=256,verbose_name="نام استاندارد")

    image = models.ImageField(upload_to="product/standard/image/",verbose_name="تصویر استاندارد")

    text = models.TextField(verbose_name="توضیحات استاندارد")

    def __str__(self):
        return str(self.name)

    class Meta :
        verbose_name = "استاندارد"
        verbose_name_plural = "استاندارد ها"


# مدل دسته بندی محصول
class Category (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    name = models.CharField(max_length=256,verbose_name="نام دسته بندی",unique=True)

    slug = models.SlugField(null=True,blank=True,allow_unicode=True)

    def __str__(self):
        return str(self.name)

    class Meta :
        verbose_name = "دسته بندی محصول"
        verbose_name_plural = "دسته بندی های محصول"

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name,allow_unicode=True)
        return super().save(*args,**kwargs)



# مدل محصول
class Product (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    category = models.ForeignKey(
        to = Category,
        on_delete = models.CASCADE,
        related_name = "products",
        verbose_name = "دسته بندی"
    )

    video = models.FileField(upload_to="product/video/",verbose_name="ویدیو")

    code = models.SlugField(verbose_name="کد انباری محصول",max_length=20)

    title = models.CharField(max_length=256,verbose_name="عنوان محصول",unique=True)

    description = models.TextField(verbose_name="توضیحات محصول")

    maintain_description = models.TextField(verbose_name="روش نگهداری محصول",null=True,blank=True)

    consumtion_order = models.TextField(verbose_name="روش مصرف",blank=True,null=True)

    immunity_description = models.TextField(verbose_name="ایمنی محصول",null=True,blank=True)

    packing_description = models.TextField(verbose_name="دسته بندی محصول",null=True,blank=True)

    standard = models.ManyToManyField(
        to = Standard ,
        verbose_name = "استاندارد ها"
    )

    class Meta :
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return f"{self.category} - {self.title}"


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
        verbose_name = "مشخصات محصول"
        verbose_name_plural = "مشخصات محصول"



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