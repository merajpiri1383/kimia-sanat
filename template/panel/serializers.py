from rest_framework import serializers
from template.panel.models import SavedPage,CompanyCard,CompanyCardsPage

class SavedPageSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = SavedPage
        exclude = ["id"]

    
# صفحه شماره کارت های شرکت 

class CardNumberSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = CompanyCard
        exclude = ["id","page"]

class CardNumbersPageSerializer (serializers.ModelSerializer) : 

    cards = CardNumberSerializer(many=True)

    class Meta : 
        model = CompanyCardsPage
        exclude = ["id"]