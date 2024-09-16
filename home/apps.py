from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
    verbose_name = "مدیرت صفحه هوم"

    def ready(self) : 
        from home import signals 