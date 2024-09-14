from django.contrib import admin
from marketing.models import Marketer,SocialMedia

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    exclude = ["id"]


# مدل بازار یاب
@admin.register(Marketer)
class MarketerAdmin(admin.ModelAdmin):
    exclude = ["id"]