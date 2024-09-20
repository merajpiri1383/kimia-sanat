from django.dispatch import receiver
from django.db.models.signals import post_save
from project.models import ProjectsPage

@receiver(post_save)
def create_projects_page_instance (sender,**kwargs) : 
    projects_page = ProjectsPage.objects.first() 

    if not projects_page : 
        ProjectsPage.objects.create()