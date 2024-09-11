from django.db import models
from uuid import uuid4
from django_jalali.db.models import jDateField


# مدل دسته بندی
class Category(models.Model)  :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    name = models.CharField(max_length=256,unique=True,verbose_name="نام دسته بندی")

    cover = models.ImageField(upload_to="category/cover/",verbose_name="کاور دسته بندی")

    class Meta :
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


    def __str__(self):
        return str(self.name)


# مدل پروژه
class Project(models.Model) :

    id = models.UUIDField(default=uuid4, primary_key=True, unique=True)

    category = models.ForeignKey(
        to = Category,
        on_delete = models.CASCADE,
        related_name = "projects",
        verbose_name = "دسته بندی پروژه"
    )

    video = models.FileField(upload_to="project/video/",verbose_name='ویدیو پروژه')

    name = models.CharField(max_length=256,verbose_name="نام پروژه",unique=True)

    description = models.TextField(verbose_name="توضیحات پروژه ")

    contractor = models.CharField(max_length=256,verbose_name="نام پیمانکار")

    launch_date = jDateField(null=True,blank=True,verbose_name="تاریخ راه اندازی")

    start_date = jDateField(null=True,blank=True,verbose_name="تاریخ ساخت")

    location = models.CharField(max_length=256,verbose_name="موقیعت")

    capacity = models.CharField(max_length=256,verbose_name="ظرفیت نامی")

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta :
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه ها"



# مدل تصویر پژوژه
class ProjectImage(models.Model) :

    id = models.UUIDField(default=uuid4, primary_key=True, unique=True)

    project = models.ForeignKey(
        to = Project,
        on_delete = models.CASCADE,
        related_name = "images",
    )

    image = models.ImageField(upload_to="project/images/",verbose_name="تصویر")

    def __str__(self):
        return f"image - {self.project.name}"

    class Meta :
        verbose_name = 'تصویر پروژه'
        verbose_name_plural = "تصاویر پروژه"