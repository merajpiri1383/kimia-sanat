from django.urls import path
from blog.api import views

urlpatterns = [

    path('list/',views.BlogListAPIView.as_view(),name="blog-list"),

    path('<slug:blog_slug>/',views.BlogPageAPIView.as_view(),name="blog-detail"),

    path('<slug:blog_slug>/comment/send/',views.SendCommentBlogAPIView.as_view(),name="comment-send-blog"),

    path('comment/<comment_id>/reply/',views.ReplyCommentAPIView.as_view(),name="comment-reply-blog"),
]