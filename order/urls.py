from django.urls import path
from order.api import views

urlpatterns = [
    
    path('list/',views.OrderListAPIView.as_view(),name="order-list"),

    path('pay-slip/list/',views.PaySlipListAPIView.as_view(),name="pay-slip-list"),

    path('pay-slip/<pay_slip_id>/',views.PaySlipDetailAPIView.as_view(),name="pay-slip-detail"),

    path('<order_id>/',views.OrderAPIView.as_view(),name="order-detail"),

    path('<order_id>/pre-invoice/',views.PreInvoiceAPIView.as_view(),name="pre-invoice"),

    path('<order_id>/send-slip/',views.SendPaySlipAPIView.as_view(),name="send-slip"),

    path('product/<product_count_id>/',views.OrderProductAPIView.as_view(),name="order-product"),
]