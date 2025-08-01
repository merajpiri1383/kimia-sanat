from django.urls import path
from blog.api import views

urlpatterns = [

    path('list/',views.BlogListAPIView.as_view(),name="blog-list"), 

    path('detail/<blog_slug>/',views.BlogPageAPIView.as_view(),name="blog-detail"),

    path('detail/<blog_slug>/save/',views.SaveBlogAPIView.as_view(),name="blog-save"),

    path('category/<category_slug>/',views.CategoryAPIView.as_view(),name="category-page"),

    path('<blog_id>/comment/send/',views.SendCommentBlogAPIView.as_view(),name="comment-send-blog"),

    path('comment/send-violation/',views.SendViolationCommentAPIView.as_view(),name="send-violation"),

    path('comment/<comment_id>/reply/',views.ReplyCommentAPIView.as_view(),name="comment-reply-blog"), 

    path('search/',views.BlogSearchAPIView.as_view(),name="blog-search"),

    path('<blog_id>/waiting-user/',views.AddUserWaitingUserBlog.as_view(),name="waiting-user"),
]