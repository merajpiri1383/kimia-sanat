from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model


@receiver(post_migrate)
def create_admin_user(sender,**kwargs) :
    user,created = get_user_model().objects.get_or_create(phone="09123456789")
    user.set_password("admin")
    user.save()