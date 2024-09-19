from django.urls import path
from order.api import views

urlpatterns = [
    
    path('list/',views.OrderListAPIView.as_view(),name="order-list"),

    path('<order_id>/',views.OrderAPIView.as_view(),name="order-detail"),

    path('product/<product_count_id>/',views.OrderProductAPIView.as_view(),name="order-product"),
]