# rest framework tools
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# models
from blog.models import Category,Blog
# serializers
from blog.api.serializers import (BlogSerializer,BlogSimpleSerializer,ModuleSerializer,CategorySerializer)
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
            "not_published" : BlogSerializer(
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