from django.urls import path
from project.api import views

urlpatterns = [

    path('category/',views.CategoriePageAPIView.as_view(),name="categories"),

    path('category/<category_id>/',views.CategoryProjectsAPIView.as_view(),name="category-page"),

    path('<project_id>/' , views.ProjectPageAPIView.as_view(),name="project-page"),
]