from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from product.models import Product,Category,types_of_product
from product.api.serializers import ProductSimpleSerializer,ProductSerializer,CategorySerializer
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from utils.views import get_ip
from user.models import Ip
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# لسیت محصولات
class ProductListAPIView(APIView) :

    @swagger_auto_schema(
        operation_summary="product list page",
        operation_description="""
        ?most-viewd=True :    پربازید ترین ها 
        ?category={category_slug} :     دسته بندی 
        ?type={product_type} :     نوع محصول
        default :  جدیدترین ها
        """
    )
    def get(self,request):
        products = Product.objects.all().order_by("-created")

        try :
            if request.GET.get("most-viewed",True):
                products = products.order_by("views")

            if request.GET.get("category"):
                category = Category.objects.get(slug=request.GET.get("category"))
                products = products.filter(category=category)

            if request.GET.get("type"):
                products = products.filter(type=request.GET.get("type"))
        except :
            return Response({'detail' : "incorrect filter ."})

        paginator = Paginator(products, 10)
        try :
            products = paginator.page(request.GET.get("page",1))
        except EmptyPage :
            products = paginator.page(1)
        except PageNotAnInteger :
            products = paginator.page(1)
        data = {
            'products' : ProductSimpleSerializer(
                products,
                many=True,
                context={'request' : request}
            ).data,
            'categories' : CategorySerializer(
                Category.objects.all(),
                many=True,
            ).data,
            'types_of_product' : types_of_product
        }
        if products.has_next() :
            print()
            data["next_page"] = (f"{request.build_absolute_uri().split("?")[0]}"
                                 f"?page={products.next_page_number()}")
        if products.has_previous() :
            data["previous_page"] = (f"{request.build_absolute_uri().split("?")[0]}"
                                     f"?page={products.previous_page_number()}")
        return Response(data,status.HTTP_200_OK)



# صفحه محصول

class ProductPageAPIView (APIView) :

    def get(self,request,slug):
        try :
            product = Product.objects.get(slug=slug)
        except :
            return Response({'detail' : 'product not found .'},status.HTTP_404_NOT_FOUND)
        ip = get_ip(request)
        if ip :
            ip,created = Ip.objects.get_or_create(ip=ip)
            product.views.add(ip)
        data = {
            'product' : ProductSerializer(product,context={'request':request}).data
        }
        return Response(data,status.HTTP_200_OK)