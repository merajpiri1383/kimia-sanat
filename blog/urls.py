from django.urls import path
from blog.api import views

urlpatterns = [

    path('list/',views.BlogListAPIView.as_view(),name="blog-list"),

]