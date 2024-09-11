from project.api.serializers import CategorySerializer,ProjectSerializer
from rest_framework.generics import ListAPIView
from project.models import Category,Project
from project.paginations import ProjectPagination
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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