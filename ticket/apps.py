from django.apps import AppConfig


class TicketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ticket'
    verbose_name = 'مدیرت تیکت ها'

    def ready(self) : 
        from ticket import signals