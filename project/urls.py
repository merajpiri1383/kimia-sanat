from django.urls import path
from project.api import views

urlpatterns = [

    path('category/',views.CategoriePageAPIView.as_view(),name="categories"),

    path('category/<category_slug>/',views.CategoryProjectsAPIView.as_view(),name="category-page"),

    path('<project_slug>/' , views.ProjectPageAPIView.as_view(),name="project-page"),

    # comment
    path('<project_slug>/comment/send/',views.SendCommentProjectAPIView.as_view(),name="send-comment-project"),

    path('comment/send-violation/',views.SendViolationCommentAPIView.as_view(),name="send-violation"),

    path('comment/<comment_id>/reply/',views.ReplyCommentAPIView.as_view(),name="reply-comment-project"),

    # save 

    path("<project_slug>/save/",views.SaveProjectAPIView.as_view(),name="save-project")
]