from django.apps import AppConfig


class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notification'
    verbose_name = 'مدیرت اعلانات'

    def ready(self) : 
        from notification import signals
