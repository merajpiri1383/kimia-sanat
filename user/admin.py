from django.contrib import admin
from user.models import User,LegalProfile,RealProfile,Marketer,SocialMedia
from django.contrib.auth.models import Group
from django.utils.html import format_html
from order.models import Order


admin.site.unregister(Group)

admin.site.site_header = " کیمیا صنعت"
admin.site.index_title = "مدیرت کیمیا صنعت"

# مدل پروفایل حقیقی
class RealProfileStackInline (admin.StackedInline) :
    model = RealProfile
    extra = 0
    exclude = ['id']

# مدل پروفایل حقوقی
class LegalProfileStackInline (admin.StackedInline) :
    model = LegalProfile
    extra = 0
    exclude = ["id"]

class OrderInline (admin.StackedInline) : 
    exclude = ['id']
    model = Order
    extra = 0

# مدل اصلی کاربر
@admin.register(User)
class UserAdmin (admin.ModelAdmin) :
    exclude = ["id","password"]
    inlines = [RealProfileStackInline,LegalProfileStackInline,OrderInline]
    list_display = ["index","phone","is_real","is_legal","username","user_type"]
    readonly_fields = ["username","user_type","index"]

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    exclude = ["id"]


# مدل بازار یاب
@admin.register(Marketer)
class MarketerAdmin(admin.ModelAdmin):
    exclude = ["id"]
    list_display = ["index","show_image","name","active_phone","type"]
    readonly_fields = ["index"]

    def show_image(self, obj):
        if obj.image:  # بررسی وجود تصویر
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "بدون تصویر"