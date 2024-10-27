from rest_framework import serializers
from template.panel.models import SavedPage

class SavedPageSerializer (serializers.ModelSerializer) : 

    class Meta : 
        model = SavedPage
        exclude = ["id"]