from django.urls import path
from product.api import views

urlpatterns = [

    path('list/',views.ProductListAPIView.as_view(),name="product-list"),

    path('<slug:slug>/',views.ProductPageAPIView.as_view(),name="product-detail"),

    path('<slug:slug>/comment/send/',views.SendCommentProductAPIView.as_view(),name="send-comment-porduct"),

    path('comment/<comment_id>/reply/',views.ReplyCommentAPIView.as_view(),name="reply-comment-product"),

    path('<slug:slug>/catalog/',views.CatalogProductAPIView.as_view(),name="product-catalog")

]