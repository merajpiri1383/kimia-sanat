from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model


@receiver(post_migrate)
def create_admin_user(sender,**kwargs) :
<<<<<<< HEAD

    try : 
        user = get_user_model().objects.get(phone="09123456789")
    except : 
=======
    try :
        user = get_user_model().objects.get(phone="09123456789")
    except :
>>>>>>> 177eeed57f8b6de7ba4dc88ad8feaed3433cd58c
        user = get_user_model().objects.create(
            phone = "09123456789",
            is_active=True,
            is_staff=True,
<<<<<<< HEAD
            is_superuser = True
=======
            is_superuser= True
>>>>>>> 177eeed57f8b6de7ba4dc88ad8feaed3433cd58c
        )
        user.set_password("admin")
        user.save()