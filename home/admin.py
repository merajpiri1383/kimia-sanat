from django.contrib import admin
from home.models import Consult


# مدل مشاوره 
@admin.register(Consult)
class ConsultAdmin (admin.ModelAdmin) : 
    exclude = ["id"]