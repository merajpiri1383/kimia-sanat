from django.contrib import admin
from config.models import (
    ContactItem,
    ContactUs,
    ContactTitle,
    SocialTitle,
    Location,
    ContactConsult
)

# مدل ارتباط با ما

class ContactTitleInline (admin.StackedInline) : 
    model = ContactTitle
    extra = 0
    exclude = ["id"]

class ContactItemInline (admin.TabularInline) : 
    model = ContactItem
    extra = 0
    exclude = ["id"]

class SocialTitleInline (admin.StackedInline) : 
    model = SocialTitle
    extra = 0
    exclude = ["id"]

class LocationInline (admin.StackedInline) : 
    model = Location
    extra = 0
    exclude = ["id"]

@admin.register(ContactUs)
class ContactUsAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [
        ContactTitleInline,
        ContactItemInline,
        SocialTitleInline,
        LocationInline
    ]


@admin.register(ContactConsult)
class ContactConsultAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    list_display = ["index","name","department","phone","email","text"]
    readonly_fields = ["index"]

    def index (self,obj )  : 
        return list(ContactConsult.objects.all()).index(obj) + 1
    index.short_description = "ردیف"