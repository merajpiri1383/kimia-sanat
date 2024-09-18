from django.urls import path
from template.api import views

urlpatterns = [
    
    path('',views.TemplateAPIView.as_view(),name="template"),
]