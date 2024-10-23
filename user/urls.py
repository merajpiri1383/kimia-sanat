from django.urls import path
from user.api import views

urlpatterns = [
    
    path('real-profile/',views.RealProfileAPIView.as_view(),name="real-profile"),

    path('legal-profile/',views.LegalProfileAPIView.as_view(),name="legal-profile"),

    path('social-media/',views.SocialMediaAPIView.as_view(),name="social-media"),

    path('saved/',views.SavedItems.as_view(),name="saved") , 

    path('comment/<comment_id>/interaction/',views.CommentInteractionAPIView.as_view(),name="comment-interaction"),

    path('dashboard/',views.DashboardAPIView.as_view(),name="dashboard"),

    path('me/',views.UserAPIView.as_view(),name="user-info")
]