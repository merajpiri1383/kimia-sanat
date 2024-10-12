from import_export import resources
from system.models import ProductSystem
from import_export import fields


class ProductSystemResource (resources.ModelResource) : 

    class Meta : 
        model = ProductSystem
        fields = ["id","product_code","name","colleague_price","buy_price"]
        export_order = ["id","product_code","name","colleague_price","buy_price"]
    
    def get_export_headers(self, fields=None):
        headers = super().get_export_headers(fields)
        for i, h in enumerate(headers):
            if h == 'id':
                headers[i] = "آیدی"
            if h == 'product_code':
                headers[i] = "کد محصول"
            if h == 'name':
                headers[i] = "نام محصول"
            if h == 'colleague_price':
                headers[i] = "قیمت همکار"
            if h == 'buy_price':
                headers[i] = "قیمت فروش"
        return headers