# rest framework tools
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
# models
from blog.models import Category,Blog,Comment
# serializers
from blog.api.serializers import (BlogSerializer,BlogSimpleSerializer,
                CategorySerializer,CommentReplySerializer,CommentSerializer,ViolationCommentSerializer) 
# swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# pagination
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.postgres.search import SearchQuery,SearchVector,SearchRank
# permissions 
from rest_framework.permissions import IsAuthenticated


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
            "pages" : paginator.num_pages,
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
    def post(self,request,blog_id):
        try :
            blog = Blog.objects.get(id=blog_id)
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
    



# سرچ بلاگ ها 
class BlogSearchAPIView (APIView) : 

    @swagger_auto_schema(
        operation_summary="جست و جوی بلاگ",
        operation_description="کلمه کلیدی با استفاده از پارامتر query مشخص میشه",
        responses={
            200 : BlogSimpleSerializer(many=True)
        }
    )
    def get(self,request) : 
        blogs = []
        query = request.GET.get("query")
        if query : 
            blogs = Blog.objects.annotate(rank=SearchRank(
                vector = SearchVector("title","description","author"),
                query = SearchQuery(query)
            )).filter(rank__gt=0.001).order_by("-rank")
        return Response(BlogSimpleSerializer(blogs,many=True,context={'request':request}).data,status.HTTP_200_OK)
    

# گزارش تخلف

class SendViolationCommentAPIView (APIView) : 
    
    @swagger_auto_schema(
        operation_summary="گزارش تخلف کامنت",
        tags=["blog / comment"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "comment" : openapi.Schema(type=openapi.TYPE_STRING,description="ایدی کامنت"),
                "topic" : openapi.Schema(type=openapi.TYPE_STRING,description="موضوع"),
                "description" : openapi.Schema(type=openapi.TYPE_STRING,description="توضیحات"),
            },
            required=["topic","description"]
        ),
        responses={
            201 : ViolationCommentSerializer(),
            400 : 'bad request'
        }
    )
    def post(self,request) : 
        serializer = ViolationCommentSerializer(data=request.data)
        if serializer.is_valid() : 
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else : 
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        

# ذخیره بلاگ ها 

class SaveBlogAPIView (APIView) : 

    permission_classes = [IsAuthenticated]

    def dispatch(self,request,blog_slug) : 
        try : 
            self.blog = Blog.objects.get(slug=blog_slug)
        except : 
            self.blog = None
        return super().dispatch(request,blog_slug)

    def post(self,request,blog_slug) : 
        if not self.blog : return Response({'detail':'blog not found .'},status.HTTP_404_NOT_FOUND)
        request.user.saved_blogs.add(self.blog)
        return Response({'message':'blog saved successfully .'},status.HTTP_200_OK)
    
    def delete(self,request,blog_slug) : 
        if not self.blog : return Response({'detail':'blog not found .'},status.HTTP_404_NOT_FOUND)
        request.user.saved_blogs.remove(self.blog)
        return Response({'message':'blog unsaved successfully .'},status.HTTP_200_OK)