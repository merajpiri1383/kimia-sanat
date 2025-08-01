from django.db import models
from uuid import uuid4
from django.utils.text import slugify
from django_jalali.db.models import jDateField
from django.core.exceptions import ValidationError
from utils.models import CommentBase
from django.contrib.auth import get_user_model



class Tag (models.Model) : 

    id = models.UUIDField(default=uuid4,unique=True,primary_key=True)

    name = models.CharField(max_length=256,verbose_name="نام برچسب")

    slug = models.SlugField(null=True,blank=True,allow_unicode=True)

    def __str__(self) : 
        return str(self.name)
    
    class Meta : 
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"
    
    def save(self,**kwargs) : 
        self.slug = slugify(self.name,allow_unicode=True)
        return super().save(**kwargs)

# مدل دسته بدی
class Category (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    name = models.CharField(max_length=256,verbose_name="دسته بندی",unique=True)

    slug = models.SlugField(null=True,blank=True,allow_unicode=True,unique=True)

    class Meta :
        verbose_name = "دسته بندی بلاگ"
        verbose_name_plural = "دسته بندی های بلاگ"

    def save(self,**kwargs):
        self.slug = slugify(self.name,allow_unicode=True)
        return super().save(**kwargs)

    def __str__(self):
        return str(self.name)


# مدل بلاگ 
class Blog (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    category = models.ForeignKey(
        to = Category,
        on_delete = models.CASCADE,
        related_name="blogs",
        verbose_name="دسته بندی"
    )

    title = models.CharField(max_length=256,unique=True,verbose_name="عنوان مقاله")

    author = models.CharField(max_length=256,verbose_name="نویسنده")

    code = models.SlugField(verbose_name="کد بلاگ",null=True,blank=True)

    slug = models.SlugField(unique=True,null=True,blank=True,allow_unicode=True)

    tag = models.ManyToManyField(Tag,blank=True,verbose_name="برچسب")

    description = models.TextField(verbose_name="توضیحات مقاله")

    created_date = jDateField(null=True,verbose_name="تاریخ انتشار",blank=True)

    cover = models.ImageField(upload_to="blog/cover",verbose_name="کاور بلاگ")

    is_published = models.BooleanField(default=False,verbose_name="ایا انتشار شده است")

    user_waiting = models.ManyToManyField(
        to=get_user_model(),
        blank=True,
        verbose_name="کاربران در انتظار"
    )

    def __str__(self) :
        return f"{self.category.name} - {self.title}"

    class Meta :
        verbose_name = "بلاگ"
        verbose_name_plural = "بلاگ ها"

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title,allow_unicode=True)
        return super().save(*args,**kwargs)


# ماژول های بلاگ
class Module (models.Model) :

    id = models.UUIDField(default=uuid4,primary_key=True,unique=True)

    blog = models.ForeignKey(
        to = Blog,
        on_delete = models.CASCADE,
        related_name = "modules",
        verbose_name = "بلاگ"
    )

    text = models.TextField(null=True,blank=True,verbose_name="متن")

    created = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"{self.blog.title} - {self.created}"

    def save(self,*args,**kwargs):
        self.clean()
        return super().save(*args,**kwargs)

    def clean(self) :
        if not self.text  and not self.file and not self.image :
            raise ValidationError("text,file,image one of them is required .")


# مدل کامنت
class Comment (CommentBase) :

    blog = models.ForeignKey(
        to = Blog,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="بلاگ",
    )

    liked_by = models.ManyToManyField(
        to=get_user_model(),
        blank=True,
        related_name="blog_comment_likeds",
        verbose_name="لایک شده توسط"
    )

    disliked_by = models.ManyToManyField(
        to=get_user_model(),
        blank=True,
        verbose_name="دیس لایک شده توسط",
        related_name="blog_comment_dislikeds"
    )

    class Meta : 
        verbose_name = "کامنت "
        verbose_name_plural = "کامنت های بلاگ"
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