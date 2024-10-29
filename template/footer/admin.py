from django.contrib import admin
from template.models import (
    CategoryFooter,
    Footer,
    FooterLink,
    PhoneFooter,
    ElectroLicense,
    FooterFeq,
    CustomerClub
)



# فوتر 

class FooterLinkInline (admin.TabularInline) : 
    model = FooterLink
    extra = 0 
    exclude = ["id"]


class PhoneFooterInline (admin.TabularInline) : 
    model = PhoneFooter
    exclude = ["id"]
    extra = 0

class CategoryFooterInline (admin.TabularInline) : 
    model = CategoryFooter
    exclude = ["id"]
    extra = 0

class ElectroLicenseInline (admin.TabularInline) : 
    model = ElectroLicense
    exclude = ["id"]
    extra = 0

class FooterFeqInline (admin.StackedInline) : 
    model = FooterFeq
    exclude = ["id"]
    extra = 0

@admin.register(Footer)
class FooterAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines= [
        FooterLinkInline,
        PhoneFooterInline,
        CategoryFooterInline,
        ElectroLicenseInline,
        FooterFeqInline
    ]


# باشگاه مشتریان
@admin.register(CustomerClub)
class CustomerClubAdmin (admin.ModelAdmin) : 
    exclude = ["id"]