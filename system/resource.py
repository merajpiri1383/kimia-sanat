from import_export import resources
from system.models import ProductSystem

class ProductSystemResource (resources.ModelResource) : 

    class Meta : 
        model = ProductSystem
        fields = ["id","group","product_code","name","colleague_price","buy_price"]
        export_order = ["id","group","product_code","name","colleague_price","buy_price"]