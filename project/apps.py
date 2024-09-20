from django.apps import AppConfig


class ProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project'
    verbose_name = "تنظیمات پروژه ها و دسته بندی پروژه ها"

    def ready(self) : 
        from project import signals