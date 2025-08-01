from django.urls import path
from order.api import views

urlpatterns = [

    path('search/',views.SearchOrderAPIView.as_view(),name="search"),

    path('product/count/',views.OrderProductCountAPIView.as_view(),name="order-product-count"),

    path('products/',views.ProductListAPIView.as_view()),
    
    path('list/',views.OrderListAPIView.as_view(),name="order-list"),

    path('info/',views.OrderTotalInfo.as_view(),name="order-total-info"),

    path('rules/',views.OrderRuleSAPIView.as_view(),name="order-rules"),

    path('completed/',views.CompletedOrdersAPIView.as_view(),name="completed-orders"),

    path('pay-slip/list/',views.PaySlipListAPIView.as_view(),name="pay-slip-list"),

    path('pay-slip/<pay_slip_id>/',views.PaySlipDetailAPIView.as_view(),name="pay-slip-detail"),

    path('<order_id>/',views.OrderAPIView.as_view(),name="order-detail"),

    path('<order_id>/pre-invoice/',views.PreInvoiceAPIView.as_view(),name="pre-invoice"),

    path('<order_id>/send-slip/',views.SendPaySlipAPIView.as_view(),name="send-slip"),
]