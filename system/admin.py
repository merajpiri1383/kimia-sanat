from django.contrib import admin
from system.models import GroupProduct,ProductSystem
import openpyxl
from django.http import HttpResponse
from django.contrib.humanize.templatetags.humanize import intcomma


@admin.register(GroupProduct)
class GroupProductAdmin (admin.ModelAdmin) : 
    exclude = ["id"]

def export_excel_action (model,request,queryset) : 
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Exported Data"

    headers = [field.name for field in ProductSystem._meta.fields]

    headers.remove("id")
    headers.remove("group")

    name_columns = [ProductSystem._meta.get_field(field).verbose_name for field in headers]
    ws.append(name_columns)

    for object in queryset : 
        row = [getattr(object,field) for field in headers]
        ws.append(row)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=export.xlsx'

    wb.save(response)
    return response

@admin.register(ProductSystem)
class ProductSystemAdmin (admin.ModelAdmin) : 
    exclude = ["id"]
    list_display = ["group","product_code","name","colleague_price_format","buy_price_format"]
    actions = [export_excel_action]

    def colleague_price_format(self,obj) :
        return intcomma(obj.colleague_price,False)
    
    def buy_price_format(self,obj) : 
        return intcomma(obj.buy_price,False)
    
    colleague_price_format.short_description = "قیمت هر کیلو گرم برای همکار(ریال)"
    buy_price_format.short_description = "قیمت هر کیلو گرم برای فروش (ریال)"

    export_excel_action.short_description = "خروجی excel"