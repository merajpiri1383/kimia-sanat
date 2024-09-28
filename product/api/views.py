from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from product.models import Product,Category,types_of_product,Comment
from product.api.serializers import (ProductSimpleSerializer,ProductSerializer,CategorySerializer,
            CommentSerializer,CommentReplySerializer)
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from utils.views import get_ip
from user.models import Ip
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def get_types_of_product () : 
    data = []
    for item in types_of_product : 
        data.append({
            "key" : str(item[0]),
            "value" : str(item[1])
        })
    return data

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
            'pages' : paginator.num_pages,
            'count' : paginator.count,
            'types_of_product' : get_types_of_product(),
        }
        if products.has_next() :
            print()
            data["next_page"] = (f"{request.build_absolute_uri().split("?")[0]}?page={products.next_page_number()}")
        if products.has_previous() :
            data["previous_page"] = (f"{request.build_absolute_uri().split("?")[0]}?page={products.previous_page_number()}")
        return Response(data,status.HTTP_200_OK)



# صفحه محصول

class ProductPageAPIView (APIView) :

    @swagger_auto_schema(
        operation_summary="product page",
        operation_description="details of product"
    )
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
            'product' : ProductSerializer(product,context={'request':request}).data,
            'comments' : CommentSerializer(
                product.comments.filter(reply_to=None),
                many=True
            ).data
        }
        return Response(data,status.HTTP_200_OK)


# ارسال کامنت برای محصول
class SendCommentProductAPIView(APIView) :

    @swagger_auto_schema(
        tags=["product / comment"],
        operation_summary="send comment",
        operation_description="send comment for product . (product page)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name' : openapi.Schema(type=openapi.TYPE_STRING,description="نام و نام خانوادگی"),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="ایمیل"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="توضیحات"),
            },
            required=["name","email","description"]
        )
    )
    def post(self,request,slug):
        try :
            product = Product.objects.get(slug=slug)
        except :
            return Response({'detail' : 'product not found .'},status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data["product"] = product.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


# پاسخ به کامنت
class ReplyCommentAPIView(APIView) :

    @swagger_auto_schema(
        tags=["product / comment"],
        operation_summary="reply comment",
        operation_description="reply comment for product . (product page)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="نام و نام خانوادگی"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="توضیحات"),
            },
            required=["name", "description"]
        )
    )
    def post(self,request,comment_id):

        try :
            comment = Comment.objects.get(id= comment_id)
        except :
            return Response({'detail':"comment not found"},status.HTTP_404_NOT_FOUND)
        data= request.data.copy()
        data["product"] = comment.product.id
        data["reply_to"] = comment_id
        serializer  = CommentReplySerializer(data=data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)