from django.apps import AppConfig

class ConfigConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'config'
    verbose_name = "تنظیمات کلی"
    def ready(self) : 
        from config import signals