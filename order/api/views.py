from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import status
from utils.permissions import IsOwnOrNot,IsActiveOrNot
from product.models import Count
from order.models import Order
from order.api.serializers import OrderSerializer,PaySlipSerializer,OrderSimpleSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# سفارش ها
class OrderListAPIView (APIView) : 

    permission_classes = [IsActiveOrNot]

    @swagger_auto_schema(
        operation_summary="لیست سفارش ها"
    )
    def get(self,request) : 
        serializer = OrderSimpleSerializer(request.user.orders.all(),many=True)
        return Response(serializer.data,status.HTTP_200_OK)
    

# مدیرت سفارش
class OrderAPIView (APIView) : 
    
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

# مدیرت محصول
class OrderProductAPIView (APIView) : 

    permission_classes = [IsOwnOrNot]

    def get_order(self,request,product_count_id) :
        try : 
            self.product = Count.objects.get(id=product_count_id)
        except : 
            return Response({'detail' : 'product count not found .'},status.HTTP_404_NOT_FOUND) 
        self.order = request.user.orders.filter(is_send=False,is_valid=False).first()
        if not self.order : 
            self.order = Order.objects.create(user=request.user)

    @swagger_auto_schema(
        operation_summary="افزودن محصول به سفارش",
        operation_description="افزودن محصول به سفارش "
    )
    def post(self,request,product_count_id) : 
        result = self.get_order(request,product_count_id)
        if result : return result
        self.order.products_count.add(self.product)
        serializer = OrderSerializer(self.order)
        return Response(serializer.data,status.HTTP_200_OK)
    

    @swagger_auto_schema(
        operation_summary="حذف محصول از سفارش",
        operation_description="حذف محصول از سفارش"
    )
    def delete(self,request,product_count_id) : 
        result = self.get_order(request,product_count_id)
        if result : return result
        self.order.products_count.remove(self.product)
        serializer = OrderSerializer(self.order)
        return Response(serializer.data,status.HTTP_200_OK) 
    
# ارسال فیش واریزی
class SendPaySlipAPIView (APIView) : 

    permission_classes = [IsOwnOrNot]

    @swagger_auto_schema(
        operation_summary="ارسال فیش واریزی",
        operation_description="ارسال فیش واریزی توسط کاربر",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description="نام و نام خانوادگی واریز کننده",
                    minLength=1,  # حداقل طول نام
                    maxLength=256  # حداکثر طول نام
                ),
                'image': openapi.Schema(
                    type=openapi.TYPE_FILE, 
                    description="تصویر فیش واریزی"
                ),
                'time': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description="تاریخ واریز",
                    format="date-time"  # فرمت تاریخ و زمان
                ),
                'order_tracking_number': openapi.Schema(
                    type=openapi.TYPE_INTEGER, 
                    description="شماره پیگیری سفارش",
                    minimum=100000,  # حداقل مقدار
                    maximum=999999  # حداکثر مقدار
                ),
                'description': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description="توضیحات",
                    minLength=0,  # حداقل طول توضیحات
                    maxLength=500  # حداکثر طول توضیحات (به طور مثال 500 کاراکتر)
                )
            }
        )
    )
    def post(self,request,order_id) : 

        try : 
            order = Order.objects.get(id=order_id)
        except : 
            return Response({'detail' : 'order not found .'},status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data["order"] = order_id
        serializer = PaySlipSerializer(data=data)
        if serializer.is_valid () :
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)