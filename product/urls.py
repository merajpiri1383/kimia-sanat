from django.urls import path
from product.api import views

urlpatterns = [

    path('list/',views.ProductListAPIView.as_view(),name="product-list"),

    path('<slug:slug>/',views.ProductPageAPIView.as_view(),name="product-detail"),
]