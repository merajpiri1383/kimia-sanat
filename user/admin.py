from django.contrib import admin
from user.models import User,LegalProfile,RealProfile,Marketer,SocialMedia
from django.contrib.auth.models import Group
from order.models import Order

admin.site.unregister(Group)


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

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    exclude = ["id"]


# مدل بازار یاب
@admin.register(Marketer)
class MarketerAdmin(admin.ModelAdmin):
    exclude = ["id"]