from project.api.serializers import (CategorySerializer,ProjectSerializer,CommentSendSerializer,
                                     ReplyCommentSerializer)
from rest_framework.generics import ListAPIView
from project.models import Category,Project,Comment
from project.paginations import ProjectPagination
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi


# صفحه دسته بندی ها
class CategoriePageAPIView(ListAPIView) :
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = ProjectPagination

    @swagger_auto_schema(
        operation_summary="categories page",
        operation_description="list of categories"
    )
    def get(self,request):
        return super().get(request) 


# صفحه پروژه
class ProjectPageAPIView(APIView) :

    @swagger_auto_schema(
        operation_summary="project page",
        operation_description="details of project",
        responses={
            200 : ProjectSerializer(),
            404 : "project not found with this id ."
        }
    )
    def get(self,request,project_id):
        try :
            object = Project.objects.get(id=project_id)
        except :
            return Response({'detail' : 'project not found .'},status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(object,context={'request': request})
        return Response(serializer.data,status.HTTP_200_OK)

# صفحه پروژه های یک دسته بندی
class CategoryProjectsAPIView(APIView) :

    @swagger_auto_schema(
        operation_summary="category page",
        operation_description="list of all project for this category",
        responses={
            200 : ProjectSerializer(many=True),
            404 : "category not found ."
        }
    )
    def get(self,request,category_id):
        try :
            object = Category.objects.get(id=category_id)
        except :
            return Response({'detail': 'category not found .'},status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(object.projects.all(),many=True,context={'request' : request})
        return Response(serializer.data,status.HTTP_200_OK)


# ارسال کامنت برای پروژه
class SendCommentProjectAPIView(APIView) :

    @swagger_auto_schema(
        tags=["project / comment "],
        operation_summary="send comment",
        operation_description="send comment for a project",
        request_body=openapi.Schema(
            type = openapi.TYPE_OBJECT,
            properties={
                "name" : openapi.Schema(type=openapi.TYPE_STRING,description="نام و نام خانوادگی"),
                "phone": openapi.Schema(type=openapi.TYPE_NUMBER, description="تلفن"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="ایمیل"),
                "text": openapi.Schema(type=openapi.TYPE_STRING, description="توضیحات"),
            },
            required=["name","phone","email","text"],
        ),
        responses={
            201 : "created",
            404 : "project not found ",
            400 : "bad data"
        }
    )
    def post(self,request,project_id):
        try :
            project = Project.objects.get(id=project_id)
        except :
            return Response({'detail' : 'project not found .'},status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data["project"] = project_id
        serializer = CommentSendSerializer(data=data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


# پاسخ به کامنت
class ReplyCommentAPIView(APIView ) :

    @swagger_auto_schema(
        tags=["project / comment "],
        operation_summary="send reply comment",
        operation_description="send reply comment for a project",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="نام و نام خانوادگی"),
                "text": openapi.Schema(type=openapi.TYPE_STRING, description="توضیحات"),
            },
            required=["name", "text"],
        ),
        responses={
            201: "created",
            404: "project not found ",
            400: "bad data"
        }
    )
    def post(self,request,comment_id):
        try :
            comment = Comment.objects.get(id=comment_id)
        except :
            return Response({'detail' : 'comment not found .'},status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data["project"] = comment.project.id
        data["reply_to"] = comment_id
        serializer = ReplyCommentSerializer(data=data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)