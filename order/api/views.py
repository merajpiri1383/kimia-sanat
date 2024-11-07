from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import status
from utils.permissions import IsOwnOrNot,IsActiveOrNot
from order.models import Order,PaySlip,Rule
from django.contrib.postgres.search import SearchQuery,SearchRank,SearchVector
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from order.api.serializers import (
    OrderSerializer,OrderSimpleSerializer,
    PreInvoiceSerializer,
    PaySlipSerializer,
    ProductCountSerializer,
    RuleSerializer,
)
from order.panel.serializers import (
    ListShopPageSerializer,
    OrderPageSerializer,
    MyOrderPageSerializer
)
from order.panel.models import ListShopPage,OrderPage,MyOrderPage
from product.models import Product
from product.api.serializers import ProductSimpleSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# سفارش ها
class OrderListAPIView (APIView) : 

    permission_classes = [IsActiveOrNot]

    @swagger_auto_schema(
        operation_summary="لیست سفارش ها",
        operation_description="""

        ?state=
            accept => تایید شده
            reject => عدم تایید
            paid => پرداخت شده
            pending => در انتظار تایید
            """
    )
    def get(self,request) : 

        state = request.GET.get("state")
        orders = request.user.orders.all().order_by("created")
        if state : 
            orders = orders.filter(state=state).order_by("created")
        paginator = Paginator(orders,5)
        try :
            result = paginator.page(request.GET.get("page",1))
        except EmptyPage : 
            result = paginator.page(1)
        except PageNotAnInteger : 
            result = paginator.page(1)
        data = {
            "result" : OrderSimpleSerializer(result,many=True,context={'request':request}).data,
            "count" : paginator.count,
            "page_nums" : paginator.num_pages,
            "next_page" : f"{request.build_absolute_uri().split("?")[0]}?page={result.next_page_number()}"
            if result.has_next() else None,
            "previous_page" : f"{request.build_absolute_uri().split("?")[0]}?page={result.previous_page_number()}"
            if result.has_previous() else None,
        }
        return Response(data,status.HTTP_200_OK)
    

# مدیرت سفارش
class OrderAPIView (APIView) : 

    permission_classes = [IsOwnOrNot]
    
    def dispatch(self,request,order_id) :
        try : 
            self.order = Order.objects.get(id=order_id)
        except : 
            self.order = None  
        return super().dispatch(request,order_id)   
    
    @swagger_auto_schema(
            operation_summary="جزییات سفارش"
    )
    def get(self,request,order_id) : 
        if not self.order : return Response({'detail' : 'order not found .'},status.HTTP_200_OK)
        self.check_object_permissions(request,self.order)
        serializer = OrderSerializer(self.order,context={'request':request})
        return Response(serializer.data,status.HTTP_200_OK)
    
    @swagger_auto_schema(
            operation_summary="تغییر سفارش"
    )
    def put(self,request,order_id) : 
        if not self.order : return Response({'detail' : 'order not found .'},status.HTTP_200_OK)
        self.check_object_permissions(request,self.order)
        serializer = OrderSerializer(instance=self.order,data=request.data)
        if serializer.is_valid () : 
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        else : 
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


# افزودن محصول از سفارش 
# اگه سفارشی که در حالت pending نداشته باشه 
# یک سفارش جدید درست میکنه

class OrderProductCountAPIView (APIView) : 

    permission_classes = [IsActiveOrNot,IsOwnOrNot]
        
    @swagger_auto_schema(
        operation_summary="افزودن محصول به سفارش",
        operation_description="""
                                id محصول رو میگیره
                                درصورتی که سفارشی داشته باشه که در وضعیت pending باشه به اون سفارش اضافه میکنه
                                در غیر این صورت یک سفارش جدید درست میکنه

                                delivery_type : 
                                    factory => ارسال از درب کارخانه توسط شرکت
                                    customer => تحویل کالا درب کارخانه توسط مشتری
                                    driver =>  معرفی راننده باربر توسط مشتری

                                delivery_times :
                                    12 => 12 ساعت
                                    24 => 24 ساعت
                                    48 => 48 ساعت
                                    72 => 72 ساعت
                                
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "products_count" : openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "product" : openapi.Schema(type=openapi.TYPE_OBJECT,description="ایدی محصول"),
                        "value" : openapi.Schema(type=openapi.TYPE_STRING,description="مقدار محصول"),
                    },
                    required=["product","value"]
                ),
                "delivery_type" : openapi.Schema(type=openapi.TYPE_STRING,description="نوع تحویل"),
                "delivery_time" : openapi.Schema(type=openapi.TYPE_STRING,description="زمان تحویل"),
                "driver" : openapi.Schema(type=openapi.TYPE_STRING,description="آیدی راننده"),
            },
            required=["products_count"]
        ),
        responses={
            201 : OrderSerializer(),
            400 : "bad requred"
        }
    )
    def post(self,request) : 
        data = request.data.copy()
        products_count = data.get("products_count")
        if not products_count : 
            return Response({"products_count":"this field is required ."})
        if not isinstance(products_count,list) : 
            return Response({"detail": "products_count must be a list"},status.HTTP_400_BAD_REQUEST)
        for item in products_count : 
            if not isinstance(item,dict) : 
                return Response({'invalid data'},status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(user=request.user)
        for item in products_count : 
            item["order"] = order.id
            serializer = ProductCountSerializer(data=item)
            if serializer.is_valid() : 
                serializer.save()
            else : 
                return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        serializer = OrderSerializer(instance=order,data=request.data,context={'request':request})
        if serializer.is_valid() : 
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        else : 
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

    
# ارسال فیش واریزی
class SendPaySlipAPIView (APIView) : 

    permission_classes = [IsOwnOrNot]

    @swagger_auto_schema(
        operation_summary="ارسال فیش واریزی",
        operation_description="ارسال فیش واریزی توسط کاربر",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'file': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description=" فیش واریزی"
                ),
            },
            required=["file"]
        )
    )
    def post(self,request,order_id) : 

        try : 
            order = Order.objects.get(id=order_id)
        except : 
            return Response({'detail' : 'order not found .'},status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data["order"] = order.id
        serializer = PaySlipSerializer(data=data)
        if serializer.is_valid () :
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        


# پیش فاکتور 

class PreInvoiceAPIView (APIView) : 

    permission_classes = [IsActiveOrNot]

    @swagger_auto_schema(
        operation_summary="پیش فاکتور سفارش",
        responses={
            200 : PreInvoiceSerializer(),
            404 : "not found ",
            400 : "pre invoice not ready",
        }
    )
    def get(self,request,order_id) : 
        order = request.user.orders.filter(id=order_id).first()
        if order : 
            if hasattr(order,"pre_invoice") : 
                serializer = PreInvoiceSerializer(order.pre_invoice)
                return Response(serializer.data,status.HTTP_200_OK)
            else : 
                return Response({'detail' : 'pre invoice not ready .'},status.HTTP_400_BAD_REQUEST)
        else : 
            return Response({'detail':'order not found .'},status.HTTP_404_NOT_FOUND)
        


# لیست فیش های واریزی 

class PaySlipListAPIView (APIView ) : 

    permission_classes = [IsActiveOrNot]

    def get(self,request) : 
        pay_slips = []
        orders = request.user.orders.all().order_by("-created")
        for order in orders : 
            for pay_slip in order.pay_slips.all().order_by("-time") : 
                pay_slips.append(pay_slip)
        print(pay_slips)
        paginator = Paginator(pay_slips,8)
        try : 
            pay_slips = paginator.page(request.GET.get("page",1))
        except EmptyPage : 
            pay_slips = paginator.page(1)
        except PageNotAnInteger : 
            pay_slips = paginator.page(1)

        data = {
            "results" : PaySlipSerializer(pay_slips,many=True,context={'request':request}).data,
            "count" : paginator.count , 
            "page_nums" : paginator.num_pages,
            "next_page" : f"{request.build_absolute_uri().split("?")[0]}?page={pay_slips.next_page_number()}" 
            if pay_slips.has_next() else None ,
            "previous_page" : f"{request.build_absolute_uri().split("?")[0]}?page={pay_slips.previous_page_number()}" 
            if pay_slips.has_previous() else None ,
        }
        return Response(data,status.HTTP_200_OK)


# جزییات فیش واریزی 

class PaySlipDetailAPIView (APIView) : 

    @swagger_auto_schema(
        operation_summary="جزییات فیش واریزی",
        responses={
            200 : PaySlipSerializer(),
            404 : "not found "
        }
    )
    def get(self,request,pay_slip_id) :
        try : 
            pay_slip = PaySlip.objects.get(id=pay_slip_id)
        except : 
            return Response({'detail' : 'pay slip not found .'},status.HTTP_404_NOT_FOUND)
        serializer = PaySlipSerializer(pay_slip,context={'request' : request})
        return Response(serializer.data,status.HTTP_200_OK) 
    


#  اطاعات کلی سفارش ها 

class OrderTotalInfo (APIView) : 

    permission_classes = [IsActiveOrNot]

    @swagger_auto_schema(
        operation_summary="اطاعات کلی سفارش ها"
    )
    def get(self,request) : 
        orders = request.user.orders
        data = {
            "all" : orders.count(),
            "accept" : orders.filter(state="accept").count(),
            "reject" : orders.filter(state="reject").count(),
            "paid" : orders.filter(state="paid").count(),
            "pending" : orders.filter(state="pending").count(),
            "page" : ListShopPageSerializer(
                ListShopPage.objects.first(),
            ).data
        }
        return Response(data,status.HTTP_200_OK)
    

# سفارش های تکمیل شده 

class CompletedOrdersAPIView (APIView) : 

    permission_classes = [IsActiveOrNot]

    @swagger_auto_schema(
        operation_summary="سوابق خرید",
    )
    def get(self,request) : 
        orders = request.user.orders.filter(state="paid").order_by("created")
        paginator = Paginator(orders,5)
        try : 
            result = paginator.page(request.GET.get("page",1))
        except EmptyPage : 
            result = paginator.page(1)
        except PageNotAnInteger : 
            result = paginator.page(1)
        data = {
            "result" : OrderSimpleSerializer(result,many=True,context={'request':request}).data,
            "page" : MyOrderPageSerializer(MyOrderPage.objects.first()).data ,
            "count" : paginator.count,
            "num_pages" : paginator.num_pages,
            "next_page" : f"{request.build_absolute_uri().split("?")[0]}?page={result.next_page_number()}" 
            if result.has_next() else None,
            "previous_page" : f"{request.build_absolute_uri().split("?")[0]}?page={result.previous_page_number()}" 
            if result.has_previous() else None
        }
        return Response(data,status.HTTP_200_OK)
    


# لیست محصولات

class ProductListAPIView (APIView) : 

    @swagger_auto_schema(
        operation_summary="لیست محصولات صفحه سفارش",
        responses={
            200 : ProductSimpleSerializer(many=True),
        }
    )
    def get(self,request) : 
        products = Product.objects.all().order_by("-created")
        data = {
            "page" : OrderPageSerializer(OrderPage.objects.first()).data,
            "products" : ProductSimpleSerializer(
                    products,
                    many=True,
                    context={'request':request}
                ).data
        }
        return Response(data,status.HTTP_200_OK)
    

# قوانین سفارش 

class OrderRuleSAPIView (APIView) : 

    @swagger_auto_schema(
        operation_summary="قوانین سفارش",
        responses={
            200 : RuleSerializer(many=True)
        }
    )
    def get(self,request) : 
        serializer = RuleSerializer(
            Rule.objects.all(),
            many=True
        )
        return Response(serializer.data,status.HTTP_200_OK)
    

# سرچ سفارش 

class SearchOrderAPIView (APIView) : 

    permission_classes = [IsActiveOrNot]

    @swagger_auto_schema(
        operation_summary="سرچ سفارش",
        operation_description="""?query=""",
        responses={
            200 : OrderSimpleSerializer(many=True)
        }
    )
    def get(self,request) : 
        result = []
        query = request.GET.get("query")
        if query : 
            result = request.user.orders.annotate(rank=SearchRank(
                query=SearchQuery(query),
                vector=SearchVector("tracking_code","created","state","delivery_time","delivery_type")
            )).filter(rank__gt=0.001).order_by("-rank")
        serializer = OrderSimpleSerializer(result,many=True,context={'request':request})
        return Response(serializer.data,status.HTTP_200_OK)