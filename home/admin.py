from django.contrib import admin
from home.models import Company,Consult,ImageCompany,License


# مدل مشاوره 
@admin.register(Consult)
class ConsultAdmin (admin.ModelAdmin) : 
    exclude = ["id"]

# تصاویر سالایدر صفحه هوم
class  ImageCompanyTabular (admin.TabularInline) : 
    model = ImageCompany
    extra = 1 
    exclude = ["id"]

# مدل شرکت
@admin.register(Company)
class ComapnyAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    inlines = [ImageCompanyTabular]


# مدل گواهی نامه ها
@admin.register(License)
class LicenseAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    search_fields = ["title","description"]