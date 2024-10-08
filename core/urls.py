from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.views.static import serve
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema = get_schema_view(
    openapi.Info(
        title="kimiya saneat",
        description="backend of kimiyasaneat built with django and django rest frame work",
        default_version="v1"
    ),
    public=True
)

urlpatterns = [

    path('admin/', admin.site.urls),

    path('config/',include('config.urls')),

    path('project/',include('project.urls')),

    path('blog/',include('blog.urls')),

    path('product/',include('product.urls')),

    path('template/',include("template.urls")),

    path('driver/',include('driver.urls')),

    path('order/',include('order.urls')),

    path('user/',include('user.urls')),

    path('auth/',include("authentication.urls")),

    path('',schema.with_ui('swagger',cache_timeout=0),name="swagger"),

    path("summernote", include("django_summernote.urls")),

    re_path('^media/(?P<path>.*)$',serve,{'document_root' : settings.MEDIA_ROOT}),
]