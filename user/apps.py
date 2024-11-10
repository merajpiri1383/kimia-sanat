from django.apps import AppConfig,apps
from django.contrib import admin



class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
    verbose_name = "مدیرت کاربران"
    def ready(self):
        from user import signals
        Attachment = apps.get_model('django_summernote', 'Attachment')
        BlacklistedToken = apps.get_model("token_blacklist","BlacklistedToken")
        OutStatingToken = apps.get_model("token_blacklist","OutstandingToken")
        try:
            admin.site.unregister(Attachment)
            admin.site.unregister(BlacklistedToken)
            admin.site.unregister(OutStatingToken)
        except admin.sites.NotRegistered:
            pass