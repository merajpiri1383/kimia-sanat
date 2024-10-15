from project.api.serializers import (CategorySerializer,ProjectSerializer,CommentSendSerializer,
            ReplyCommentSerializer,ProjectsPageSerializer,ProjectSimpleSerializer,ViolationCommentSerializer)
from project.models import Category,Project,Comment,ProjectsPage
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from rest_framework.permissions import IsAuthenticated


# صفحه دسته بندی ها
class CategoriePageAPIView(APIView) : 

    @swagger_auto_schema(
        operation_summary="categories page",
        operation_description="list of categories"
    )
    def get(self,request):
        paginator = Paginator(Category.objects.all().order_by("-name"),per_page=10)
        try :
            categories = paginator.page(request.GET.get("page",1))
        except EmptyPage : 
            categories = paginator.page(1)
        except PageNotAnInteger : 
            categories = paginator.page(1)
        data = {
            'page_titles' : ProjectsPageSerializer(ProjectsPage.objects.first(),context={'request':request}).data,
            'categories' : CategorySerializer(
                categories,
                many=True,
                context={'request' : request}
            ).data,
            'pages' : paginator.num_pages
        }
        if categories.has_next() : 
            data["next_page"] = f"{request.build_absolute_uri().split("?")[0]}?page={categories.next_page_number()}"
        
        if categories.has_previous() :
            data["previous_page"] = f"{request.build_absolute_uri().split("?")[0]}?page={categories.previous_page_number()}"
        return Response(data,status.HTTP_200_OK)


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
    def get(self,request,project_slug):
        try :
            object = Project.objects.get(slug=project_slug)
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
            200 : ProjectSimpleSerializer(many=True),
            404 : "category not found ."
        }
    )
    def get(self,request,category_slug):
        try :
            object = Category.objects.get(slug=category_slug)
        except :
            return Response({'detail': 'category not found .'},status.HTTP_404_NOT_FOUND)
        data = {
            'category' : CategorySerializer(object,context={'request': request}).data,
            'projects' : ProjectSimpleSerializer(object.projects.all(),many=True,context={'request' : request}).data,
        }
        return Response(data,status.HTTP_200_OK)


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
    def post(self,request,project_slug):
        try :
            project = Project.objects.get(slug=project_slug)
        except :
            return Response({'detail' : 'project not found .'},status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data["project"] = project.id
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
        

# گزارش تخلف

class SendViolationCommentAPIView (APIView) : 
    
    @swagger_auto_schema(
        operation_summary="گزارش تخلف کامنت",
        tags=["project / comment "],
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
        

# ذخیره پروژه

class SaveProjectAPIView (APIView) : 

    permission_classes = [IsAuthenticated]

    def dispatch(self, request, project_slug):
        try : 
            self.project = Project.objects.get(slug=project_slug)
        except : 
            self.project = None
        return super().dispatch(request,project_slug)

    def post(self,request,project_slug) : 
        if not self.project : return Response({'detail':'project not found .'},status.HTTP_404_NOT_FOUND)
        request.user.saved_projects.add(self.project)
        return Response({'message':'project saved successfully .'},status.HTTP_200_OK)
    
    def delete (self,request,project_slug) : 
        if not self.project : return Response({'detail':'project not found .'},status.HTTP_404_NOT_FOUND)
        request.user.saved_projects.remove(self.project)
        return Response({'message': 'project unsaved successfully .'},status.HTTP_200_OK)