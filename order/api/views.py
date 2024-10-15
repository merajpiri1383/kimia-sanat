from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import status
from utils.permissions import IsOwnOrNot,IsActiveOrNot
from product.models import Count
from order.models import Order,PaySlip
from order.api.serializers import (
    OrderSerializer,OrderSimpleSerializer,
    PreInvoiceSerializer,
    PaySlipSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger





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