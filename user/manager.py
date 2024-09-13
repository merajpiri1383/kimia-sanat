from django.contrib.auth.models import BaseUserManager


class UserManager (BaseUserManager) :

    def create_user (self,phone,password=None,**kwargs) :

        user = self.model(phone=phone,**kwargs)
        if password :
            user.set_password(password)
        return user.save()


    def create_superuser(self,phone,password,**kwargs):

        kwargs.setdefault("is_active",True)
        kwargs.setdefault("is_staff",True)
        kwargs.setdefault("is_superuser",True)

        if not kwargs.get("is_active") :
            return ValueError("is_active must be true .")

        if not kwargs.get("is_staff") :
            return ValueError("is_staff must be true .")

        if not kwargs.get("is_superuser") :
            return ValueError("is_superuser must be true .")

        return self.create_user(phone,password,**kwargs)