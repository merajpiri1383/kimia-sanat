# rest framework tools
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# models
from blog.models import Category,Blog,Comment
# serializers
from blog.api.serializers import (BlogSerializer,BlogSimpleSerializer,
                CategorySerializer,CommentReplySerializer,CommentSerializer) 
# swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# pagination
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# python tools
from datetime import datetime


# لسیت مقالات
class BlogListAPIView(APIView) :

    def get(self,request):
        paginator = Paginator(Blog.objects.filter(is_published=True).order_by("-created_date"),6)
        try :
            blogs = paginator.page(request.GET.get("page",1))
        except EmptyPage :
            blogs = paginator.page(1)
        except PageNotAnInteger :
            blogs = paginator.page(1)
        data = {
            "blogs" : BlogSimpleSerializer(blogs,many=True,context={"request":request}).data,
            "count" : paginator.count,
            "not_published" : BlogSimpleSerializer(
                Blog.objects.filter(is_published=False).order_by("-created_date")[:3],
                many=True,
                context={'request' : request}
            ).data,
            "categories" : CategorySerializer(
                Category.objects.all(),
                many=True
            ).data
        }
        if blogs.has_next() :
            print()
            data["next_page"] = f"{request.build_absolute_uri().split("?")[0]}?page={blogs.next_page_number()}"
        if blogs.has_previous() :
            data["previous_page"] = f"{request.build_absolute_uri().split("?")[0]}?page={blogs.previous_page_number()}"
        return Response(data,status.HTTP_200_OK)
    

# صفحه داخلی بلاگ
class BlogPageAPIView(APIView) : 

    def get(self,request,blog_slug) : 
        try : 
            blog = Blog.objects.get(slug=blog_slug)
        except :
            return Response({'detail' : "blog not found ."},status.HTTP_404_NOT_FOUND)
        data = {
            'blog' : BlogSerializer(blog,context={'request':request}).data,
            "not_published" : BlogSimpleSerializer(
                Blog.objects.filter(is_published=False).order_by("-created_date")[:3],
                many=True,
                context={'request' : request}
            ).data,
            "categories" : CategorySerializer(
                Category.objects.all(),
                many=True
            ).data,
            'newest' : BlogSimpleSerializer(
                Blog.objects.filter(is_published=True).exclude(id=blog.id).order_by("-created_date")[:4],
                many=True,
                context={'request':request}
            ).data,
            'comments' : CommentSerializer(
                blog.comments.filter(reply_to=None),
                many=True,
            ).data
        }
        return Response(data,status.HTTP_200_OK) 
    

# ارسال کامنت برای محصول
class SendCommentBlogAPIView(APIView) :

    @swagger_auto_schema(
        tags=["blog / comment"],
        operation_summary="send comment",
        operation_description="send comment for blog . (blog page)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name' : openapi.Schema(type=openapi.TYPE_STRING,description="نام و نام خانوادگی"),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="ایمیل"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="توضیحات"),
            },
            required=["name","email","description"]
        )
    )
    def post(self,request,blog_slug):

        print(blog_slug)
        try :
            blog = Blog.objects.get(slug=blog_slug)
        except :
            return Response({'detail' : 'blog not found .'},status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data["blog"] = blog.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


# پاسخ به کامنت
class ReplyCommentAPIView(APIView) :

    @swagger_auto_schema(
        tags=["blog / comment"],
        operation_summary="reply comment",
        operation_description="reply comment for blog . (blog page)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="نام و نام خانوادگی"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="توضیحات"),
            },
            required=["name", "description"]
        )
    )
    def post(self,request,comment_id):

        try :
            comment = Comment.objects.get(id= comment_id)
        except :
            return Response({'detail':"comment not found"},status.HTTP_404_NOT_FOUND)
        data= request.data.copy()
        data["blog"] = comment.blog.id
        data["reply_to"] = comment_id
        serializer  = CommentReplySerializer(data=data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        

# صفحه داخلی دسته بندی

class CategoryAPIView (APIView) : 

    @swagger_auto_schema(
        operation_description="صفحه داخلی دسته بندی",
        operation_summary="صفحه دسته بندی"
    )
    def get(self,request,category_slug) : 
        try :
            category = Category.objects.get(slug=category_slug)
        except :
            return Response({'detail':'category not found .'},status.HTTP_404_NOT_FOUND)
        paginator = Paginator(category.blogs.filter(is_published=True).order_by("-created_date"),per_page=10)
        try :
            blogs = paginator.page(request.GET.get("page",1))
        except EmptyPage : 
            blogs = paginator.page(1)
        except PageNotAnInteger : 
            blogs = paginator.page(1)
        data = {
            'page_titles' : BlogsPageSerializer(BlogsPage.objects.first(),context={'request':request}).data,
            'categories' : CategorySerializer(Category.objects.all()[:6],many=True).data,
            'blogs' : BlogSimpleSerializer(
                blogs,
                many=True,
                context={'request' : request}
            ).data,
            'pages' : paginator.num_pages
        }
        if blogs.has_next() : 
            data["next_page"] = f"{request.build_absolute_uri().split("?")[0]}?page={blogs.next_page_number()}"
        if blogs.has_previous() : 
            data["previous_page"] = f"{request.build_absolute_uri().split("?")[0]}?page={blogs.previous_page_number()}"
        return Response(data,status.HTTP_200_OK)