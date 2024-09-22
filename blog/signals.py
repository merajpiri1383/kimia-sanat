from django.dispatch import receiver
from django.db.models.signals import post_migrate
from blog.models import BlogsPage

@receiver(post_migrate)
def create_blogs_page_instance (sender,**kwargs) :
    blogs_page = BlogsPage.objects.first()
    if not blogs_page : 
        BlogsPage.objects.create()