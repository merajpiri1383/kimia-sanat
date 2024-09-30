from django.urls import path
from product.api import views

urlpatterns = [

    path('<product_id>/comment/send/',views.SendCommentProductAPIView.as_view(),name="send-comment-porduct"),

    path('comment/<comment_id>/reply/',views.ReplyCommentAPIView.as_view(),name="reply-comment-product"),

    path('list/',views.ProductListAPIView.as_view(),name="product-list"),

    path('<slug>/',views.ProductPageAPIView.as_view(),name="product-detail"),

    path("<product_slug>/like/",views.LikedProductAPIView.as_view(),name="product-like"),
]