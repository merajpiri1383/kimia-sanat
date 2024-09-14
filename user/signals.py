from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model


@receiver(post_migrate)
def create_admin_user(sender,**kwargs) :

    try : 
        user = get_user_model().objects.get(phone="09123456789")
    except : 
        user = get_user_model().objects.create(
            phone = "09123456789"
            is_active=True,
            is_staff=True,
            is_superuser = True
        )
        user.set_password("admin")
        user.save()