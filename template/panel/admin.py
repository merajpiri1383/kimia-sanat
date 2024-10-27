from django.contrib import admin
from template.panel.models import CompanyCard,CompanyCardsPage,SavedPage

# صفحه شماره کارت ها

class CardNumberInline (admin.StackedInline) : 
    model = CompanyCard
    extra = 0
    exclude = ["id"]

@admin.register(CompanyCardsPage)
class CompanyCardsPageAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [CardNumberInline]


@admin.register(SavedPage)
class SavedPageAdmin (admin.ModelAdmin) : 
    exclude = ["id"]