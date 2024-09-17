from django.apps import AppConfig


class TemplateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'template'
    verbose_name = "مدیرت صفحه اصلی"
    
    def ready(self) -> None:
        from template import signals